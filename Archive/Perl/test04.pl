use Graph::Easy;

my $g = Graph::Easy->new();
$g->set_attribute('flow', 'south');
# print $g->flow();

my $a = $g->add_node('Main App');
my $b = $g->add_node('Sim calcs');
$b->relative_to($a, 10, 0);
my $e = $g->add_edge($a,$b);
# $e->set_attribute('edge_flow', 'south');
print $e->edge_flow();

my $c = $g->add_node('Gen reports');
$c->relative_to($b, 10, 0);
$g->add_edge($b,$c);
my $o = $g->add_node('Update 2D graphics');
$g->add_edge($o,$b);
# print $g->as_svg();
print $g->as_boxart();
