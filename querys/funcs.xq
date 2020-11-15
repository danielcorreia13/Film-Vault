module namespace funcs = "funcs";

declare function funcs:filmsOrderByYearPage($page, $n,$syear, $fyear, $categories) as element()*
{
  <root>
  {
  let $cat := tokenize($categories, ' ')
  let $films := 
                for $film in collection('Films')//movie
                order by $film/year
                where $film/year >= $syear and $film/year <= $fyear
                for $genre in $film/genres//item
                where contains($cat, data($genre)) 
                return $film
                
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover-url>{ data($film/cover-url) }</cover-url>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//name , 0, 5)
          }
          </actors>
          <directors>{
          $film/directors//name
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 3) }</genres>
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByYearPage($page, $n, $categories) as element()*
{
   <root>
  {
  let $cat := tokenize($categories, ' ')
  let $films := 
                for $film in collection('Films')//movie
                order by $film/year
                for $genre in $film/genres//item
                where contains($cat, data($genre)) 
                return $film
                
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover-url>{ data($film/cover-url) }</cover-url>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//name , 0, 5)
          }
          </actors>
          <directors>{
          $film/directors//name
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 3) }</genres>
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByYearPage( $page, $n, $syear, $fyear) as element()*
{
  <root>
  {
  let $films := 
                for $film in collection('Films')//movie
                order by $film/year
                where $film/year >= $syear and $film/year <= $fyear
                return $film
                
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover-url>{ data($film/cover-url) }</cover-url>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//name , 0, 5)
          }
          </actors>
          <directors>{
          $film/directors//name
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 3) }</genres>
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByYearPage($page, $n) as element()*
{
   <root>
  {
  let $films := for $film in collection('Films')//movie
                order by $film/year
                return $film
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover-url>{ data($film/cover-url) }</cover-url>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//name , 0, 5)
          }
          </actors>
          <directors>{
          $film/directors//name
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 3) }</genres>
         </elem>
  }
  </root>
};

declare function funcs:getFilms() as element()*
{
  <root>
  {
  for $film in collection("Films")//movie
  return <elem>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover-url>{ data($film/cover-url) }</cover-url>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//name , 0, 5)
          }
          </actors>
          <directors>{
          $film/directors//name
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 3) }</genres>
         </elem>
  }
  </root>
};
