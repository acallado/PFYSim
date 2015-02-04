use Graph::Easy;
use open ':std', ':encoding(UTF-8)';

my $g = Graph::Easy->new();
$g->set_attribute('flow', 'south');
# print $g->flow();

my $a = $g->add_node('Main App');

my $an01 = $g->add_anon_node();

my $d = $g->add_node('2D Graphics');
$d->relative_to($a, 5, -5);
my $h = $g->add_edge($an01,$d);
$h->set_attribute('start', 'east');

my $b = $g->add_node('Sim calcs');
$b->relative_to($a, 5, -1);
my $i = $g->add_edge($a,$b);
$i->set_attribute('start', 'east');

my $c = $g->add_node('Reports');
$c->relative_to($a, 5, 0);
my $j = $g->add_edge($a,$c);
$j->set_attribute('start', 'east');


# my $c = $g->add_node('Gen reports');
# my $f = $g->add_edge($b,$c);
# $f->set_attribute('flow', 'south');
# # $f->set_attribute('min_len', '3');

# my $o = $g->add_node('Update 2D graphics');
# # $o->relative_to($b, 10, 5);
# $o->set_attribute('rotate', '45');
# $o->set_attribute('offset', '10, -50');
# my $h = $g->add_edge($b, $o);
# # $h->set_attribute('flow', 'east');

# my $p = $g->add_node('Check iteration');
# $o->set_attribute('offset', '10, -50');
# $p->set_attribute('rotate', '45');
# my $i = $g->add_edge($b, $p);
# $i->set_attribute('flow', 'west');

# my $q = $g->add_node('Output message');
# my $j = $g->add_edge($b, $q);
# $j->set_attribute('flow', 'west');

$g->layout();

print $g->as_svg();
# print $g->as_boxart();
# print $g->as_ascii();
