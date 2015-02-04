# creating a graph from a textual description
use Graph::Easy::Parser;
use Graph::Easy::As_svg;
my $parser = Graph::Easy::Parser->new();

my $graph = $parser->from_text('
[ Bonn ] --> [ Koblenz ] --> { minlen: 3; } [ Frankfurt ]
  --> [ Dresden ]

[ Koblenz ] --> [ Trier ] { origin: Koblenz; offset: 2, 2; }
  --> [ Frankfurt ]');
# print $graph->as_boxart();

my $graph2 = $parser->from_text('
[ Main ]
[ ] [ Load .CFG ] { origin: [ ]; offset: 2, 2; } <--> [ Main ] ');
# print $graph2->as_boxart();
print $graph->as_svg_file();

# print $parser->from_file('mygraph.txt')->as_ascii();

# Also works automatically on graphviz code:
# print Graph::Easy::Parser->from_file('mygraph.dot')->as_ascii();
