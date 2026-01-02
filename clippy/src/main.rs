use clap::{Parser, Subcommand};
use notify_rust::Notification;
use std::fs;
use std::path::PathBuf;
use std::thread;
use std::time::Duration;

const POWER_SUPPLY_PATH: &str = "/sys/class/power_supply";
const POWERCAP_PATH: &str = "/sys/class/powercap";
const SAMPLE_DURATION_MS: u64 = 1000;

#[derive(Parser)]
#[command(name = "clippy")]
#[command(about = "A helpful command-line utility", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Notify,
    Power,
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Notify => run_notify(),
        Commands::Power => run_power(),
    }
}

fn run_notify() {
    Notification::new()
        .summary("Hello from Clippy!")
        .body("This is a test notification")
        .icon("dialog-information")
        .show()
        .expect("Failed to show notification");

    println!("Notification sent!");
}

fn run_power() {
    let mut results = Vec::new();

    if let Ok(battery_power) = measure_battery_power() {
        results.push(battery_power);
    }

    if let Ok(rapl_power) = measure_rapl_power() {
        results.extend(rapl_power);
    }

    if results.is_empty() {
        eprintln!("No power consumption data available");
    } else {
        for result in results {
            println!("{}", result);
        }
    }
}

fn measure_battery_power() -> Result<String, String> {
    let power_supply_dir = PathBuf::from(POWER_SUPPLY_PATH);

    if !power_supply_dir.exists() {
        return Err("Power supply directory not found".to_string());
    }

    let battery = find_battery(&power_supply_dir)?;
    let battery_path = power_supply_dir.join(&battery);

    let read_value = |filename: &str| -> Result<f64, String> {
        let file_path = battery_path.join(filename);
        fs::read_to_string(&file_path)
            .map_err(|_| format!("Cannot read {}", filename))
            .and_then(|s| {
                s.trim()
                    .parse::<f64>()
                    .map_err(|_| format!("Cannot parse {}", filename))
            })
    };

    let charge1 = read_value("charge_now").or_else(|_| read_value("energy_now"))?;
    let voltage1 = read_value("voltage_now")?;

    thread::sleep(Duration::from_millis(SAMPLE_DURATION_MS));

    let charge2 = read_value("charge_now").or_else(|_| read_value("energy_now"))?;
    let voltage2 = read_value("voltage_now")?;

    let time_hours = SAMPLE_DURATION_MS as f64 / 3_600_000.0;

    let energy1 = charge1 * voltage1 / 1_000_000_000_000.0;
    let energy2 = charge2 * voltage2 / 1_000_000_000_000.0;
    let power = (energy1 - energy2) / time_hours;

    let status = fs::read_to_string(battery_path.join("status"))
        .unwrap_or_else(|_| "Unknown".to_string())
        .trim()
        .to_string();

    Ok(format!("Battery ({}): {:.2} W", status, power.abs()))
}

fn find_battery(power_supply_dir: &PathBuf) -> Result<String, String> {
    let entries = fs::read_dir(power_supply_dir)
        .map_err(|e| format!("Failed to read power supply directory: {}", e))?;

    for entry in entries {
        let entry = entry.map_err(|e| format!("Failed to read entry: {}", e))?;
        let path = entry.path();

        if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
            let type_path = path.join("type");
            if let Ok(device_type) = fs::read_to_string(&type_path) {
                if device_type.trim() == "Battery" {
                    return Ok(name.to_string());
                }
            }
        }
    }

    Err("No battery found".to_string())
}

fn measure_rapl_power() -> Result<Vec<String>, String> {
    let powercap_dir = PathBuf::from(POWERCAP_PATH);

    if !powercap_dir.exists() {
        return Err("Intel RAPL not available".to_string());
    }

    let mut zones = Vec::new();

    if let Ok(entries) = fs::read_dir(&powercap_dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                if name.starts_with("intel-rapl:")
                    && name.chars().filter(|c| *c == ':').count() == 1
                {
                    zones.push(path);
                }
            }
        }
    }

    if zones.is_empty() {
        return Err("No RAPL zones found".to_string());
    }

    let mut results = Vec::new();

    for zone_path in zones {
        if let Ok(power) = measure_rapl_zone(&zone_path) {
            let zone_name = fs::read_to_string(zone_path.join("name"))
                .unwrap_or_else(|_| "Unknown".to_string())
                .trim()
                .to_string();

            results.push(format!("CPU {} power: {:.2} W", zone_name, power));
        }
    }

    if results.is_empty() {
        Err("Could not read RAPL data (may need sudo)".to_string())
    } else {
        Ok(results)
    }
}

fn measure_rapl_zone(zone_path: &PathBuf) -> Result<f64, String> {
    let energy1 = read_energy(zone_path)?;
    thread::sleep(Duration::from_millis(SAMPLE_DURATION_MS));
    let energy2 = read_energy(zone_path)?;

    let time_seconds = SAMPLE_DURATION_MS as f64 / 1000.0;
    let energy_diff = if energy2 >= energy1 {
        energy2 - energy1
    } else {
        let max_energy = read_max_energy(zone_path).unwrap_or(u64::MAX as f64);
        (max_energy - energy1) + energy2
    };

    Ok(energy_diff / time_seconds / 1_000_000.0)
}

fn read_energy(zone_path: &PathBuf) -> Result<f64, String> {
    let energy_path = zone_path.join("energy_uj");
    fs::read_to_string(&energy_path)
        .map_err(|_| "Cannot read energy (try with sudo)".to_string())
        .and_then(|s| {
            s.trim()
                .parse::<f64>()
                .map_err(|_| "Cannot parse energy".to_string())
        })
}

fn read_max_energy(zone_path: &PathBuf) -> Result<f64, String> {
    let max_energy_path = zone_path.join("max_energy_range_uj");
    fs::read_to_string(&max_energy_path)
        .map_err(|_| "Cannot read max energy".to_string())
        .and_then(|s| {
            s.trim()
                .parse::<f64>()
                .map_err(|_| "Cannot parse max energy".to_string())
        })
}
