use Graph::Easy;

my $g = Graph::Easy->new();
my $a = $g->add_node('A');
my $b = $g->add_node('B'); $b->relative_to($a, 1, 0);
my $c = $g->add_node('C'); $c->relative_to($b, 1, 0);
my $o = $g->add_node('1'); $g->add_edge($o,$c);
# print $g->as_svg();
print $g->as_boxart();
