# Design

This includes my design thoughts on various features

## Installing Binaries

### manifest file

There is a file that is stored in the ~/bin/ file, called .ytlaces-manifest.yaml. This file is used to keep track of the binaries that have been installed by the install-base.py script.

The file includes the url of the previously extracted binary. It is used to check if the new url is different from the old url, and if so, it will extract the new binary.

The manifest file takes the form of:

```yaml
binaries:
  bazelisk:
    url: https://github.com/bazelbuild/bazelisk/releases/download/v1.26.0/bazelisk-linux-amd64
  # and more, keyed by the name.
```