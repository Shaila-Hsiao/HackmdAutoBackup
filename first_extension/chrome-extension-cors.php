<?php
/**
* Plugin Name:       Chrome Extension CORS
* Description:       Enable GET requests for any chrome extensions using the REST API
* Version:           1.0.0
* Requires at least: 5.2
* Requires PHP:      7.2
* Author:            me
* Text Domain:       chrome_extension_cors
* License:           GPL v2 or later
* License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
*/

function chrome_extension_cors_rest_send_cors_headers() {
  function is_chrome_extension() {
    $chrome = "chrome-extension://";
    $origin = get_http_origin();
    return substr($origin, 0, strlen($chrome)) === $chrome;
  }

  function allow_access( $filter ) {
    header( 'Access-Control-Allow-Origin: *');
        header( 'Access-Control-Allow-Methods: OPTIONS, GET' );
    return $filter;
  }

  if (is_chrome_extension()) {
    add_filter( 'rest_pre_serve_request', 'allow_access' );
  }
}
add_action( 'rest_api_init', 'chrome_extension_cors_rest_send_cors_headers');