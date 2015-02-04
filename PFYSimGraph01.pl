#!/usr/bin/perl
use strict;
use warnings;
use Graph::Easy;
use open ':std', ':encoding(UTF-8)';


# Initialize graph
my $g = Graph::Easy->new();

# Set graph general flow
$g->set_attribute('flow', 'south');

# Add top node
my $a = $g->add_node('Main Sim App');

# Add second node
my $b = $g->add_node('Sim Modules');
# $b->relative_to($a, 0, 0);
my $e001 = $g->add_edge($a, $b);
$e001->set_attribute('start', 'south');
$e001->set_attribute('label', '.CFG file');

# Add Sim Modules children
# Dbl cycle
my $c = $g->add_node('Double Cycle List Generator');
$c->relative_to($b, 10, -1);
my $e002 = $g->add_edge($b, $c);
$e002->set_attribute('start', 'east');
$e002->set_attribute('end', 'west');
$e002->set_attribute('label', 'Sim parameters');

# Discrete Simulation Setup
my $d = $g->add_node('Discrete Simulation Setup');
$d->relative_to($c, 0, 2);
my $e003 = $g->add_edge($c, $d);
$e003->set_attribute('start', 'south');
$e003->set_attribute('end', 'north');
$e003->set_attribute('label', 'FOB action list');

# Run simulation
my $h = $g->add_node('Run Simulation');
$h->relative_to($d, 0, 2);
my $e004 = $g->add_edge($d, $h);
$e004->set_attribute('start', 'south');
$e004->set_attribute('end', 'north');
$e004->set_attribute('label', 'Discrete event simulation environment');
my $e005 = $g->add_edge($h, $b);
$e005->set_attribute('start', 'west');
$e005->set_attribute('end', 'east');
$e005->set_attribute('label', 'Sim output arrays');

# Update 2D graphics
my $i = $g->add_node('Update 2D graphics');
$i->relative_to($h, 0, 2);
my $e006 = $g->add_edge($h, $i);
$e006->set_attribute('start', 'south');
$e006->set_attribute('end', 'north');
# $e006->set_attribute('label', '');

# Add fourth node
my $f = $g->add_node('Report Modules');
$f->relative_to($b, 0, 5);
my $e007 = $g->add_edge($b, $f);
$e007->set_attribute('start', 'south');

# Add Report Modules children


$g->layout();


# print $ARGV[0];
# Print function definition
sub Print() {
    if (defined($ARGV[0]) && $ARGV[0] eq 's') {
        my $filename = 'PFYSIMStructure_'.int(rand(1000000)).'.svg';
        open(
            my $fh, '>', $filename
            ) or die "Could not open file '$filename' $!";
        print $fh $g->as_svg();
    } else {
        print $g->as_boxart();
    }
}

Print();

# print $g->as_ascii();

# my $an01 = $g->add_anon_node();
# $an01->relative_to($a, 3, 0);
# my $k = $g->add_edge($a, $an01);
# $k->set_attribute('start', 'east');
