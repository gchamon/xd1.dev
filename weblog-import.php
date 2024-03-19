<?php

# Hello from omg.lol! Questions? Email help@omg.lol.

// ensure compatibility with files containing unicode characters
shell_exec('git config core.quotepath off');

// Check for the reset trigger
$diff = shell_exec('git diff --name-only HEAD^..HEAD');
if ($diff == '') {
    echo '*** No changes detected. Are you running the latest version of the action? See https://github.com/neatnik/weblog.lol for details.';
} else {
    $diff = explode("\n", $diff);
    echo "\n*** Checking for reset request...";
    foreach ($diff as $file) {

        if (strtolower($file) == 'configuration/reset' || strtolower($file) == 'weblog/configuration/reset') {
            echo "\n*** Reset request found. Resetting...";
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, 'https://api.omg.lol/address/' . $argv[1] . '/weblog/reset');
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
            curl_setopt($ch, CURLOPT_POSTFIELDS, null);
            curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BEARER);
            curl_setopt($ch, CURLOPT_XOAUTH2_BEARER, $argv[2]);
            $response = curl_exec($ch);
            curl_close($ch);

            $diff = shell_exec('git ls-files');
            $diff = explode("\n", $diff);

            echo "\n*** Rebuilding with these entries:\n";
            print_r($diff);
            $reset = true;
            goto reset;
        }
    }
}

if (!function_exists('mime_content_type')) {

    function mime_content_type($filename)
    {

        $mime_types = array(

            'txt' => 'text/plain',
            'htm' => 'text/html',
            'html' => 'text/html',
            'php' => 'text/html',
            'css' => 'text/css',
            'js' => 'application/javascript',
            'json' => 'application/json',
            'xml' => 'application/xml',
            'swf' => 'application/x-shockwave-flash',
            'flv' => 'video/x-flv',

            // images
            'png' => 'image/png',
            'jpe' => 'image/jpeg',
            'jpeg' => 'image/jpeg',
            'jpg' => 'image/jpeg',
            'gif' => 'image/gif',
            'bmp' => 'image/bmp',
            'ico' => 'image/vnd.microsoft.icon',
            'tiff' => 'image/tiff',
            'tif' => 'image/tiff',
            'svg' => 'image/svg+xml',
            'svgz' => 'image/svg+xml',

            // archives
            'zip' => 'application/zip',
            'rar' => 'application/x-rar-compressed',
            'exe' => 'application/x-msdownload',
            'msi' => 'application/x-msdownload',
            'cab' => 'application/vnd.ms-cab-compressed',

            // audio/video
            'mp3' => 'audio/mpeg',
            'qt' => 'video/quicktime',
            'mov' => 'video/quicktime',

            // adobe
            'pdf' => 'application/pdf',
            'psd' => 'image/vnd.adobe.photoshop',
            'ai' => 'application/postscript',
            'eps' => 'application/postscript',
            'ps' => 'application/postscript',

            // ms office
            'doc' => 'application/msword',
            'rtf' => 'application/rtf',
            'xls' => 'application/vnd.ms-excel',
            'ppt' => 'application/vnd.ms-powerpoint',

            // open office
            'odt' => 'application/vnd.oasis.opendocument.text',
            'ods' => 'application/vnd.oasis.opendocument.spreadsheet',
        );

        $exploded_filename = explode('.', $filename);
        $ext = strtolower(array_pop($exploded_filename));
        if (array_key_exists($ext, $mime_types)) {
            return $mime_types[$ext];
        } elseif (function_exists('finfo_open')) {
            $finfo = finfo_open(FILEINFO_MIME);
            $mimetype = finfo_file($finfo, $filename);
            finfo_close($finfo);
            return $mimetype;
        } else {
            return 'application/octet-stream';
        }
    }
}

function get_file_contents_with_header($file)
{
    $file_contents = file_get_contents($file);
    if (!str_ends_with($file, ".md") || !str_ends_with($file, ".markdown")) {
        $mime_type = mime_content_type($file);
        $filename = basename($file);
        $header = "Type: file
Content-Type: $mime_type
Title: $filename
Location: /$filename
        
";
        return $header . $file_contents;
    } else {
        return $file_contents;
    }
}

// Now process all of the other changed content
$diff = shell_exec('git diff --name-only HEAD^..HEAD');
if ($diff == '') {
    echo "\n*** No changes detected. Are you running the latest version of the action? See https://github.com/neatnik/weblog.lol for details.";
} else {
    $diff = explode("\n", $diff);

    echo "\n*** These items have changed with this push:\n";
    print_r($diff);

    reset:

    foreach ($diff as $file) {

        if ($file == '') {
            continue;
        }

        // remove quotes from filename
        if (substr($file, 0, 1) == '"') $file = substr($file, 1);
        if (substr($file, -1) == '"') $file = substr($file, 0, -1);

        $folders_to_sync = array("weblog/", "configuration/", "css/", "js/");
        $check_sync = function (callable $comparator) use ($file) {
            return function ($should_sync, $substring) use ($file, $comparator) {
                return $should_sync ? $should_sync : $comparator($file, $substring);
            };
        };
        $should_sync_file = array_reduce($folders_to_sync, $check_sync('str_starts_with'), false);

        if ($should_sync_file === false) {
            echo "\n*** $file not in one of the dirs " . implode(" or ", $folders_to_sync) . "; skipping...";
            continue;
        }

        echo "\n*** Examining file: $file...";

        if (strtolower($file) == 'configuration/configuration.txt' || strtolower($file) == 'weblog/configuration/configuration.txt') {
            $configuration_update = $file;
            echo "\n*** Caught a configuration change. This will be triggered at the very end.";
            continue;
        }
        if (strtolower($file) == 'configuration/template.html' || strtolower($file) == 'weblog/configuration/template.html') {
            echo "\n*** Updating template...";
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, 'https://api.omg.lol/address/' . $argv[1] . '/weblog/template');
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents($file));
            curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BEARER);
            curl_setopt($ch, CURLOPT_XOAUTH2_BEARER, $argv[2]);
            $response = curl_exec($ch);
            curl_close($ch);
            continue;
        }

        $extensions_to_sync = array(".md", ".markdown", ".js", ".css");
        $should_sync_ext = array_reduce($extensions_to_sync, $check_sync('str_ends_with'), false);
        if ($should_sync_ext === false) {
            echo "\n*** $file doesn’t end in " . implode(" or ", $extensions_to_sync) . "; skipping.";
            continue;
        }

        $filename = $file;
        $filename = str_replace('/', '_', $filename);
        $filename = substr($filename, 7); // removes 'weblog_'
        $filename = substr($filename, 0, -3);

        if (file_exists($file)) {
            echo "\n*** Updating file: $file...";
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, 'https://api.omg.lol/address/' . $argv[1] . '/weblog/entry/' . urlencode($filename));
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, get_file_contents_with_header($file));
            curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BEARER);
            curl_setopt($ch, CURLOPT_XOAUTH2_BEARER, $argv[2]);
            $response = curl_exec($ch);
            curl_close($ch);
        } else {
            echo "\n*** Deleting file: $file...";
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, 'https://api.omg.lol/address/' . $argv[1] . '/weblog/delete/' . $filename);
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
            curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BEARER);
            curl_setopt($ch, CURLOPT_XOAUTH2_BEARER, $argv[2]);
            $response = curl_exec($ch);
            curl_close($ch);
        }
    }
    // save the configuration for last, since it will trigger a rebuild
    if (isset($configuration_update)) {
        echo "\n*** Updating configuration...";
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://api.omg.lol/address/' . $argv[1] . '/weblog/configuration');
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents($configuration_update));
        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BEARER);
        curl_setopt($ch, CURLOPT_XOAUTH2_BEARER, $argv[2]);
        $response = curl_exec($ch);
        curl_close($ch);
    }
}

echo "\n*** Entry processing complete. Have a nice day.";
