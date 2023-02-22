use warnings;
use strict;

use URI;
use Furl;
use File::JSON::Slurper qw/read_json write_json/;
use JSON::XS;

# Install dependencies: cpanm URI Furl File::JSON::Slurper JSON::XS
# Run: perl find_lat_lon.pl

my $furl = Furl->new;

my $db = read_json("./eczane_in.json");
my $total_count = scalar @$db;
my $no_coordinates_count = grep { !$_->{coordinates} } @$db;
my $found_count = 0;

print "TOTAL: $total_count\n";
print "No coordinates: $no_coordinates_count\n";

foreach my $pharmacy (@$db) {
  next if $pharmacy->{coordinates};
  my $name  = $pharmacy->{name};
  my $adres = $pharmacy->{extended_data}{"Açık Adres"}
            || $pharmacy->{extended_data}{Adres}
            || $pharmacy->{extended_data}{ADRES};

  my $uri = URI->new("https://nominatim.openstreetmap.org/search?format=json&country=Turkey&q=$name, $adres");
  my $response = $furl->get($uri);
  my $content  = $response->content;
  my $json     = eval { decode_json($content) };

  if (@$json){
    my $lat = $json->[0]->{lat};
    my $lon = $json->[0]->{lon};
    $pharmacy->{coordinates} = {lat => $lat, lng => $lon};
    $found_count++;
    next;
  }

  # No result. Try with Name + last word of Adres
  $adres =~ s/.*\W(\w)/$1/;

  $uri = URI->new("https://nominatim.openstreetmap.org/search?format=json&country=Turkey&q=$name, $adres");
  $response = $furl->get($uri);
  $content  = $response->content;
  $json     = eval { decode_json($content) };

  if (@$json){
    my $lat = $json->[0]->{lat};
    my $lon = $json->[0]->{lon};
    $pharmacy->{coordinates} = {lat => $lat, lng => $lon};
    $found_count++;
  }

}

print "Found: $found_count\n";
write_json("eczane_out.json", $db);