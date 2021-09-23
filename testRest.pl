#!/usr/bin/perl

# Quick Perl script to test the response from the Web APP.

use strict;
use warnings;

use Data::Dumper;

use Getopt::Long;

use HTTP::Request;
use HTTP::Response;
use HTTP::Status qw( :constants status_message );

use List::Util qw( max min );

use LWP::UserAgent;

use POSIX qw( strftime );

use Time::HiRes qw( gettimeofday );


# Preset the default running options.

my $WHATAMI = "Web API Test";


# Set Dumper for sorted keys.
$Data::Dumper::Indent = 1;
$Data::Dumper::Sortkeys = 1;


# Define config keys of interest.
my @keys = qw(
    url
);

# Labels sorted by key.
my $key_labels = {
    url             =>  "* URL to fetch (GET)",
};


# Default options.
# Only add key / value pairs where a default is wanted.
# Better to have no key than an undefined value.
my $defaults = {
    url             =>  "http://localhost:8000",
};


# Command line options.
my $cmd_options = {};


my ( $ret, $help ) = (0, 0);


my $time_before = gettimeofday();


# Read the command line and override default options.

$ret = GetOptions(
    'url=s'         =>  \$$cmd_options{url},

    'help|?'        =>  \$help,
);


# Force flush on every write to STDOUT.
$| = 1;


# Remove keys from command line options hash with no corresponding value.
while ( my ($key, $value) = each %{$cmd_options} ) {
    delete $$cmd_options{$key} unless defined $value;
}


# Set runtime config options.
my $options = { %$defaults, %$cmd_options };


sub get_max_hash_width {
    my ($hash, %options) = @_;

    # Get maximum value width from hash values.

    # Default is an empty hash.
    $hash //= {};

    # Get the options.
    my $mode = lc ($options{mode} // "value");

    my $heading = $options{heading} // undef;
    my $headings = $options{headings} // undef;

    my @keys = (defined $options{keys}) ? @{$options{keys}} : (keys %$hash);

    # Preset no width.
    my $width = 0;

    # Check if headings were supplied.
    if ( (defined $headings) && (defined $heading) ) {
        $width = length($$headings{$heading}) // 0;
    }

    # Loop through the hash keys, updating the maximum length of the key or value.
    if ($mode eq "key") {
        $width = max ($width, map { length $_ } @keys);
    }
    else {
        $width = max ($width, map { length ( $$hash{$_} // "" )  } @keys);
    }

    return $width;
}


# Work out the widths for value display.
# Negative numbers are left aligned.
my $headings = {
    label       =>  "Option",
    default     =>  "Default",
    command     =>  "Command line",
    final       =>  "Option (Final)",
};


my $wid_label = -get_max_hash_width($key_labels, keys => \@keys, heading => "label", headings => $headings);
my $wid_default = -get_max_hash_width($defaults, keys => \@keys, heading => "default", headings => $headings);
my $wid_command = -get_max_hash_width($cmd_options, keys => \@keys, heading => "command", headings => $headings);
my $wid_final = -get_max_hash_width($options, keys => \@keys, heading => "final", headings => $headings);


sub report_running_options {

    # Report running options.

    my $log_text = sprintf("[%s] Starting %s %s with parameters (* = mandatory option):

  Help              [%d] [%s]

",
            strftime("%a,%d-%b-%Y %X %Z", localtime), $WHATAMI, $0,
            $help, ($help) ? "Yes" : "No" );

    $log_text .= sprintf("%${wid_label}s  %${wid_default}s   %${wid_command}s   %${wid_final}s\n",
            $$headings{label}, $$headings{default}, $$headings{command}, $$headings{final});

    foreach my $key (@keys) {
        $log_text .= sprintf("%${wid_label}s [%${wid_default}s] [%${wid_command}s] [%${wid_final}s]\n",
                $$key_labels{$key},
                $$defaults{$key} // "",
                $$cmd_options{$key} // "",
                $$options{$key} // "" );
    }

    $log_text .= "\n";

    print $log_text;
}


# Tell people what we are doing.
report_running_options();


# Print help.
sub print_help {

    print STDERR <<HELP;

Usage: $0
        [-?|--help]
        --url="..."

$WHATAMI employs HTTP Request / Response to verify that the round loop REST GET is successful, and display the details of the request / response.

Options:
    -?|--help
        Display this help and exit.

    --url="..."
        URL to GET via REST.
        Default is [$$defaults{url}].

HELP

    return;
}


# Check if help requested.
if ($help) {
    print_help();
    exit 0;
}

# Check for missing mandatory options - print help.
my $missing = "";

my $url = $$options{url};
$missing .= "--url is missing\n" unless $url;


# Have we got missing options?
if ($missing) {
    print STDERR sprintf("ERROR: Missing mandatory options\n%s\n", $missing);
    print_help();
    exit 1;
}


# Instantiate the User Agent.
my $user_agent = new LWP::UserAgent;


# Build the HTTP request.
my $method = "GET";
my @request = ($method, $url);

my $request = new HTTP::Request(@request);

print sprintf("\n####
HTTP Request: [%s]
####\n", Dumper($request));


# Send the HTTP request and capture the response.
my $response = $user_agent->request($request);

print sprintf("\n####
HTTP Response: [%s]
####\n", Dumper($response));


# Output data from the Request / Response.
my $status = $response->code;

my $statusLine = $response->status_line;

my $statusType = "Unknown";
if ( $response->is_info ) {
    $statusType = "Informational";
}
elsif ( $response->is_success ) {
    $statusType = "Success";
}
elsif ( $response->is_redirect ) {
    $statusType = "Redirect";
}
elsif ( $response->is_client_error ) {
    $statusType = "Client Error";
}
elsif ( $response->is_server_error ) {
    $statusType = "Server Error";
}
elsif ( $response->is_error ) {
    $statusType = "Error";
}

print sprintf("\n####
testREST result:

Request:
    Method  [%s]
    URL     [%s]

Response:
    Status  [%s]
      Line  [%s]
      Type  [%s]
    Content [%s]
####\n",
        $method, $url, $status, $statusLine, $statusType, $response->content // "");


my $elapsed = gettimeofday() - $time_before;

print STDERR sprintf("\n[%s] Ending %s %s after running for [%.3f] seconds\n",
        strftime("%a,%d-%b-%Y %X %Z", localtime), $WHATAMI, $0, $elapsed);

exit 0;