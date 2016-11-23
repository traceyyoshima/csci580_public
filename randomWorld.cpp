#include <gtkmm.h>
#include <stdlib.h>
#include <vector>

using namespace std;
using namespace Gtk;

bool draw( const Cairo::RefPtr<Cairo::Context> &cr, Gtk::DrawingArea *drawarea )
{
  int n = 21;
  vector<vector<int> > squares( n, vector<int>( n ) );
  for ( unsigned int i = 0; i < n; ++i )
    for ( unsigned int j = 0; j < n; ++j )
      squares[i][j] = rand() % 4;

  Allocation allocation = drawarea->get_allocation();
  const int width = allocation.get_width();
  const int height = allocation.get_height();
  for ( int i = 0; i < n; ++i )
  {
    for ( int j = 0; j < n; ++j )
    {
      if ( squares[i][j] == 0 )
        cr->set_source_rgb( 1, 0, 0 );
      else if ( squares[i][j] == 1 )
        cr->set_source_rgb( 0, 0.33, 0 );
      else if ( squares[i][j] == 2 )
        cr->set_source_rgb( 0, 0.66, 0 );
      else
        cr->set_source_rgb( 0, 1, 0 );
      cr->rectangle( 20 * ( j + 1 ), 20 * ( i + 1 ), 19, 19 );
      cr->fill();
    }
  }
  return true;
}

int main( int argc, char *argv[] )
{
  Main kit( argc, argv );
  Window window;
  window.set_default_size( 500, 500 );
  DrawingArea drawarea;

  drawarea.signal_draw().connect(
      sigc::bind( sigc::ptr_fun( &draw ), &drawarea ) );
  window.add( drawarea );
  window.show_all();

  Main::run( window );
  return 0;
}
