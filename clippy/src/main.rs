use notify_rust::Notification;

fn main() {
    Notification::new()
        .summary("Hello from Clippy!")
        .body("This is a test notification")
        .icon("dialog-information") // This uses a standard icon
        .show()
        .expect("Failed to show notification");

    println!("Notification sent!");
}
