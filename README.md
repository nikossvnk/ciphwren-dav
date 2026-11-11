<p align="center">
  <img width="120" src="icon.svg" />
  <h1 align="center">Ciphwren DAV</h1>
</p>

> [!NOTE]
> **This is an independent fork** of [etesync-dav](https://github.com/etesync/etesync-dav), the original
> project of the EteSync authors. This fork is not affiliated with, endorsed by or supported by EteSync or
> Etebase in any way. The history of the original project is kept as it is, with its authors, and the
> changes of this fork follow it. Like the original, it's licensed under the [GPL-3.0](./LICENSE) license.

Ciphwren DAV is a CalDAV and CardDAV adapter for Etebase (EteSync 2.0) accounts, e.g. on
[Ciphwren Server](https://github.com/nikossvnk/ciphwren-server).

This package provides a local CalDAV and CardDAV server that acts as an EteSync compatibility layer (adapter).
It's meant for letting desktop CalDAV and CardDAV clients such as Thunderbird, Outlook and Apple Contacts connect with EteSync.

If all you want is to access your data from a computer, you are probably better off using the Ciphwren Web app.

# Installation

The easiest way to start using ciphwren-dav is by getting one of the pre-built binaries from the [releases page](https://github.com/nikossvnk/ciphwren-dav/releases).

These binaries are self-contained and can be run as-is, though they do not start automatically on boot. You'd need to either start them manually, or set up [autostart based on your OS](#autostart-on-system-boot).

For Linux users there's a [short installation guide](https://github.com/etesync/etesync-dav/wiki/Installing-EteSync-DAV-on-Linux) in the wiki.

# Configuration and running

1. Run `ciphwren-dav` and open the management UI in your browser: http://localhost:37358/
2. Add your EteSync user through the web UI.
3. Copy the DAV specific password by click the "Copy Password" button next to your newly added username.

For advanced usage and CLI instructions please refer to [the advanced usage section](#advanced-usage).

*Please note that some antivirus/internet security software may block the CalDAV/CardDAV service from running - make sure that ciphwren-dav is whitelisted.*

Don't forget to set up Ciphwren DAV to automatically start on startup. Instructions for this are unfortunately OS dependent and out of scope for this README.

## Common environment variables

(Before the rename they were named `ETESYNC_…`, which are still read when the `CIPHWREN_…` one isn't set.)

* `CIPHWREN_LISTEN_ADDRESS`: a hostname or IP address to listen on. Requests to a different host/ip will be block for the admin UI. Uses as the default value for the next setting.
* `CIPHWREN_SERVER_HOSTS`: defaults to `{CIPHWREN_LISTEN_ADDRESS}:37358`. Otherwise, a list of IP masks, hostnames, and ports for the server to listen on. E.g. `0.0.0.0:37358,[::]:37358` for listening on all ipv4 and ipv6 addresses and port 37358, or `localhost:37358` to only allow requests from localhost.

# Setting up clients

You now need to set up your CalDAV/CardDAV client using your username and the password you got in the previous step.

Depending on the client you use, the server path should either be:

* `http://localhost:37358/`
* `http://localhost:37358/YOUR-USERNAME/`

On most clients this should automatically detect your collections (i.e.
calendars and address books).

If your client does not automatically detect your collections, you will
need to manually add them. You can find the links in the management UI
when you click on your username.

## Specific client notes and instructions

### Thunderbird

#### Thunderbird (using native CalDAV and CardDAV support available as of [Thunderbird 91](https://support.mozilla.org/en-US/kb/new-thunderbird-91)) - preferred

##### To add calendars
1. Add a calendar by hitting the "+" symbol in the toolbar that is usually on the left of Thunderbird's Calendar view, or right-click for the context menu and select "New Calendar"
2. Select the "On the Network" radio button
3. For Username put the name of your local Etesync account
4. For Location, you will get the information from Etesync. Head to http://localhost:37358/.web/login/ and log in
5. Then click the link to collection list
6. Then copy the link for the calendar you're trying to add, and put that in for Location in the Thunderbird dialog
7. Click "Find Calendars"
8. You will see a "Password Required" popup. You need to get the password from the Etesync web interface. Go back to http://localhost:37358/.web/ and click the "Copy Password" button. Paste this password in the Thunderbird popup.
9. Hit Subscribe and you are finished, that calendar is added
10. Repeat for any additional calendars

##### To add address books
1. Click the "Address Book" icon in Thunderbird's mail view to open the Address Book
2. Within the Address Book, click File-->New-->CardDAV Address Book
3. For Username put the name of your local Etesync account
4. For Location, you will get the information from Etesync. Head to http://localhost:37358/.web/login/ and log in
5. Then click the link to collection list
6. Then copy the link for the address book you're trying to add, and put that in for Location in the Thunderbird dialog
7. Click "Continue"
8. You will see a "Password Required" popup. You need to get the password from the Etesync web interface. Go back to http://localhost:37358/.web/ and click the "Copy Password" button. Paste this password in the Thunderbird popup.
9. Hit Subscribe and you are finished, that address book is added
10. Repeat for any additional address books

#### Thunderbird (using TbSync, for Thunderbird older than version 91)
1. Install [TbSync](https://addons.thunderbird.net/en-us/thunderbird/addon/tbsync/) and the accompanying [DAV provider](https://addons.thunderbird.net/en-us/thunderbird/addon/dav-4-tbsync/).
2. Open the TbSync window: Edit -> TbSync
3. Add new DAV account (choose manual configuration).
4. Use `http://localhost:37358/` for both servers, your EteSync username as the username and the DAV password you got in [configuration and running](#configuration-and-running) as the password.

**Note:** if you enabled SSL in ciphwren-dav, you should follow the [TbSync instructions for self-signed certificates](https://github.com/jobisoft/TbSync/wiki/How-to-use-TbSync-with-self-signed-or-otherwise-untrusted-certificates%3F).

#### Thunderbird (no additional add-ons, for Thunderbird older than version 91)
TbSync includes address book support (Lightning does not), automatically discovers all your calendars/address books/tasks, and just works better in general than this solution for versions of Thunderbird older than 91. However, you *can* also do the following:

1. Install a CardDAV add-on such as Cardbook if you want to sync your contacts
2. Open http://localhost:37358 in a browser, log in with your username and account password (not encryption password), and click on the link to your DAV colection to see a list of all the calendars, tasks lists, and address books in that collection
3. For each item in the collection that you want to sync, copy the \[link] address and subscribe to that address in Thunderbird using `File > New Calendar > On the Network > CalDav` for calendars and tasks, or `New Address Book > Remote > CardDav` in Cardbook for address books

### Evolution / GNOME Contacts / GNOME Calendar
GNOME Contacts does not support adding remote address books directly, but you can add them in Evolution and they will appear correctly in all the apps. GNOME Calendar does support adding webdav calendars directly in GNOME Calendar. Calendars can also be added in Evolution and they will appear correctly in all the apps.

1. Open Evolution and click File -> New -> Collection account
2. Put your username in the user field.
3. Click Advanced Options and use `http://localhost:37358/` as the server.
4. Make sure "Look up for a CalDAV/CardDAV server" is ticked, and untick all the rest.
5. Click "Look Up" and when prompted, the DAV password you got in [configuration and running](#configuration-and-running).
6. Click Next/Finish until done.

### Windows 10 (Outlook, Windows Calendar and Windows People)
While EteSync-DAV works great on Windows 10, due to bugs in Windows itself, the instructions require a few extra steps for syncing with Outlook, Windows Calendar and Windows people. Other clients, such as Thunderbird, do no require these extra steps.

Please take a look at the [Windows 10 instructions](https://github.com/etesync/etesync-dav/wiki/Windows-10-instructions) for more information.

### macOS (Contacts.app and Calendar.app)
While EteSync-DAV works great on macOS, due to bugs in macOS Mojave, the instructions require a few extra steps for syncing with Contacts.app and Calendar.app. Other clients, such as Thunderbird, do no require these extra steps.

Please take a look at the [macOS instructions](https://github.com/etesync/etesync-dav/wiki/MacOS-instructions) for more information.

### iOS

By default, iOS only syncs events 30 days old and newer, which may look as if
events are not showing. To fix this, got to: Settings -> Calendar -> Sync and
change to the wanted time duration.

Or better yet, just use the [EteSync iOS client](https://github.com/etesync/ios).

## Autostart on system boot

It's probably easier to just follow [these instructions](https://www.howtogeek.com/228467/how-to-make-a-program-run-at-startup-on-any-computer/) for setting up autostart. Alternatively, you can try following the instructions below.

### Linux (systemd)

Make sure you have `/usr/lib/systemd/user/etesync-dav.service` on your system (should be there when installing from your distro's package manager), and then, to start the service:
`systemctl --user start ciphwren-dav`
To enable auto-start on boot:
`systemctl --user enable ciphwren-dav`

### macOS

Make sure you installed `ciphwren-dav.app` by dragging it to your `Applications` directory through finder.
Enable autostart by for example following [these instructions](https://www.howtogeek.com/228467/how-to-make-a-program-run-at-startup-on-any-computer/).

### Windows

Follow [these instructions](https://www.howtogeek.com/228467/how-to-make-a-program-run-at-startup-on-any-computer/).

# Alternative Installation Methods

This methods are not as easy as the pre-built binaries method above, but are also simple. Please follow the instructions below, following which follow the instructions in the [Configuration and running](#configuration-and-running) section.

## Docker

Run one time initial setup to persist the required configuration into a docker volume. Check out the configuration section for more information.

    docker build -t ciphwren-dav https://github.com/nikossvnk/ciphwren-dav.git
    docker run -it --rm -v ciphwren-dav:/data ciphwren-dav manage add USERNAME

Run ciphwren-dav in a background docker container with configuration from previous step. This will (re)start the container on boot and after crashes.

    docker run --name ciphwren-dav -d -v ciphwren-dav:/data -p 37358:37358 --restart=always ciphwren-dav
    
After this, refer to the [Setting up clients](#setting-up-clients) section and start using it!

### Updating

To update it, build the image again (as above), then remove the container and run it again:

    docker build -t ciphwren-dav https://github.com/nikossvnk/ciphwren-dav.git

## Arch Linux

The package `etesync-dav` is [available on AUR](https://aur.archlinux.org/packages/etesync-dav/).

The package comes with a systemd unit. To see the status of the systemd service, run:

    systemctl --user status ciphwren-dav

To inspect the logs, run:

    journalctl --user -xeu ciphwren-dav

## Windows systems

You can either follow the Docker instructions above (get Docker [here](https://www.docker.com)), or alternatively install Python3 for windows from [here](https://www.python.org/downloads/windows).

## Python virtual environment (Linux, BSD and Mac)

Install virtual env (for **Python 3**) from your package manager, for example:

- Arch Linux: pacman -S python-virtualenv
- Debian/Ubuntu: apt-get install python3-virtualenv

The below commands will install etesync to a directory called `venv` in the local path. To install to a different location, just choose a different path in the commands below.

Set up the virtual env:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install etesync-dav

The etesync-dav on PyPI doesn't have this fork's fixes for Python 3.11 and newer, so on those install
from a checkout of this repository instead:

    pip install -r requirements.txt
    pip install --no-deps .

Python 3.14 isn't supported yet: the Radicale version ciphwren-dav uses doesn't start on it.

Run the etesync commands as explained in the [Configuration and running](#configuration-and-running) section:

    ./venv/bin/etesync-dav manage ...
    ./venv/bin/etesync-dav ...

Please note that you'll have to run `source venv/bin/activate` every time you'd like to run the EteSync commands.

# Advanced usage

## CLI

1. Open a terminal and navigate to the binary's location by typing `cd /path/to/file` (most likely `cd ~/Downloads`).
2. Rename the binary to `ciphwren-dav` for ease of use, by e.g: `mv linux-ciphwren-dav ciphwren-dav`
3. Make it executable: `chmod +x ciphwren-dav`

You need to first add a user using `./ciphwren-dav manage`, for example:

`./ciphwren-dav manage add --server-url https://etebase.example.com/ USERNAME`

*Substitute `USERNAME` with your account's username, and the URL with the URL of your server.*

and then run the server:
`./ciphwren-dav`

**Note:** if you are using this with the legacy etesync server you should also pass `--legacy`

## Self-hosting

There is no default server: enter your server's URL when adding your account (`--server-url`, or
the "Server URL" field of the web UI). Alternatively, you can set the default URL to be used by
setting the `CIPHWREN_URL` environment variable to the URL of your server when running
ciphwren-dav. (`ETESYNC_URL`, its name before the rename, still works.)

## Using a proxy

EteSync-DAV should automatically use the system's proxy settings if set correctly. Alternatively, you can set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables to manually set the proxy settings.

## Self Signed Certs

If the etesync backend server is using self signed certs, the DAV bridge may refuse to connect. To solve this, run the following commands prior to starting the DAV bridge.

`export REQUESTS_CA_BUNDLE=/path/to/your/certificate.pem`

or

`export SSL_CERT_FILE=/path/file.crt`

Alternatively, if the security of certificate is not an issue (say the server is on a private network and not publicly accessible), you can ignore the certificate completely with the following commands prior to starting the DAV bridge.

```bash
export CURL_CA_BUNDLE='';
export REQUESTS_CA_BUNDLE='';
```

## Debugging

In order to put `ciphwren-dav` in debug mode so it print extra debug information please pass it the `-D` flag like so:

```bash
./etesync-dav -D
```

While this works on Linux, BSD and macOS, the Windows pre-compiled binary is compiled in "no console" mode, which means
it can't print to the terminal. In order to get the debug information on Windows, please redirect the output log to
file, like so:

```bash
set CIPHWREN_LOGFILE=output.log
ciphwren-dav.exe -D
```

## Data files

`ciphwren-dav` stores data in the directory specified by the `CIPHWREN_DATA_DIR`
environment variable. This includes a database and the credentials cache.

`CIPHWREN_DATA_DIR` defaults to a subdirectory of the appropriate data directory
for your platform. For example:
1. `~/.local/share/etesync-dav` on Linux.
2. `~/Library/Application Support/etesync-dav` on macOS
3. `C:\Documents and Settings\<User>\Application Data\Local Settings\ciphwren\ciphwren-dav` on older Windows
4. `C:\Users\<User>\AppData\Local\ciphwren\ciphwren-dav` on Windows 7 and up (Most likely)

The data of a version from before the rename (in the same places, named `etesync-dav`, and under
`etesync` on Windows) is moved to the new one the first time it starts.

See the [appdirs](https://pypi.python.org/pypi/appdirs) module docs for mor examples.

# Credits

This depends on the [Radicale server](https://radicale.org) for operation.
