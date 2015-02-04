# creating a graph from a textual description
use Graph::Easy::Parser;
my $parser = Graph::Easy::Parser->new();

my $graph = $parser->from_text(
        '[ Bonn ] -> { style: bold; label: foo; } [ Berlin ]'.
        '[ Berlin ] -> [ Rostock ]');
print $graph->as_ascii();

# print $parser->from_file('mygraph.txt')->as_ascii();

# Also works automatically on graphviz code:
# print Graph::Easy::Parser->from_file('mygraph.dot')->as_ascii();
