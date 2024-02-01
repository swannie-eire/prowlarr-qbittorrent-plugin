### THIS REPO IS NO LONGER MAINTAINED. 
### For a supported plugin please use Jackett.





**qBittorrent** comes with a few search plugins. Although these are enough for most users, if you wish to add more search engines, you can download **Prowlarr** configure the **prowlarr qBittorrent plugin** (essentially, set the API key).

**[prowlarr](https://github.com/prowlarr/prowlarr)** is a server program that provides support for more than 400 torrent sites (public and private). You may download the plugin at [this address](https://raw.githubusercontent.com/swannie-eire/prowlarr-qbittorrent-plugin/main/prowlarr.py).

### Disable the prowlarr plugin
By default, the prowlarr plugin is enabled in qBittorrent. If you want to disable it, follow these steps:
1. In the `Search tab`, click the `Search plugins...` button (bottom-right)
2. Right click on the `prowlarr` plugin
3. Uncheck the `Enabled` checkbox
4. Close the modal window

### Configuration file
The prowlarr plugin uses an external configuration file. This allows to update the plugin without losing the settings.

The file `prowlarr.json` should be located in the qBittorrent search engines folder:
* Windows: `%localappdata%\qBittorrent\nova3\engines\`
* Linux: `~/.local/share/data/qBittorrent/nova3/engines/`, or `~/.local/share/qBittorrent/nova3/engines/`, or `~/.var/app/org.qbittorrent.qBittorrent/data/qBittorrent/nova3/engines` if using Flatpak
* OS X: `~/Library/Application Support/qBittorrent/nova3/engines/`

Note: If the file doesn't exist, you can create it by copying the following JSON:

```json
{
    "api_key": "YOUR_API_KEY_HERE", 
    "tracker_first": false, 
    "url": "http://127.0.0.1:9696"
}
```

Note 3: Remember to [start prowlarr](https://github.com/prowlarr/prowlarr) first. :)

Note 4: If running qBittorrent headless and using the web page on a remote server, prowlarr needs to be configured to allow remote calls and its IP. Eg:

```json
$ cat config/data/qBittorrent/nova3/engines/prowlarr.json
{
    "api_key": "YOUR_API_KEY_HERE",
    "tracker_first": false,
    "url": "http://yourserverip:9696"
}
```

### Configuration properties
| Property |  Default value |  Description |
|---|---|---|
| api_key | YOUR_API_KEY_HERE | prowlarr API Key (you can find it int Settings > General > Security) |
| tracker_first | false | (false/true) add tracker name to the beginning of search result |
| url | http://127.0.0.1:9696 | prowlarr URL (without the end slash) |

API Key in prowlarr web UI:

![](https://i.imgur.com/ePMq68M.png)

### Screenshot
![](https://i.imgur.com/a6WPJC8.png)
