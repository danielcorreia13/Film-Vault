module namespace funcs = "funcs";

declare function funcs:filmsOrderByYearPage($search, $page, $n,$syear, $fyear, $categories) as element()*
{
  <root>
  {
  let $cats := tokenize($categories, ' ')
  let $films := 
                for $film in collection('Films')//movie
                order by $film/year descending
                where $film/year >= $syear and $film/year <= $fyear
                for $genre in $film/genres//item
                for $cat in $cats
                where contains($cat, data($genre))
                where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
                return $film

  let $count := count($films)
                
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByYearPage($search, $page, $n, $categories) as element()*
{
   <root>
  {
  let $cats := tokenize($categories, ' ')
  let $films := 
                for $film in collection('Films')//movie
                order by $film/year  descending
                for $genre in $film/genres//item
                for $cat in $cats
                where $cat = data($genre)
                where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
                return $film
  let $count := count($films)

  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByYearPage( $search, $page, $n, $syear, $fyear) as element()*
{
  <root>
  {
  let $films := 
                for $film in collection('Films')//movie
                order by $film/year descending
                where $film/year >= $syear and $film/year <= $fyear
                where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
                return $film
  let $count := count($films)
                
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByYearPage( $search, $page, $n) as element()*
{
  <root>
  {
    let $films :=
            for $film in collection('Films')//movie
            order by $film/year descending
            where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
            return $film
  let $count := count($films)
  for $film in subsequence($films, $page*$n+1, $n)
  return 
         <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};







declare function funcs:filmsOrderByAlfaPage($search, $page, $n,$syear, $fyear, $categories) as element()*
{
  <root>
  {
  let $cats := tokenize($categories, ' ')
  let $films := 
                for $film in collection('Films')//movie
                order by $film/original-title
                where $film/year >= $syear and $film/year <= $fyear
                for $genre in $film/genres//item
                for $cat in $cats
                where contains($cat, data($genre)) 
                where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
                return $film

  let $count := count($films)
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByAlfaPage($search, $page, $n, $categories) as element()*
{
   <root>
  {
  let $cats := tokenize($categories, ' ')
  let $films := 
                for $film in collection('Films')//movie
                order by $film/original-title
                for $genre in $film/genres//item
                for $cat in $cats
                where contains($cat, data($genre)) 
                where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
                return $film
  let $count := count($films)
                
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByAlfaPage( $search, $page, $n, $syear, $fyear) as element()*
{
  <root>
  {
  let $films := 
                for $film in collection('Films')//movie
                order by $film/original-title
                where $film/year >= $syear and $film/year <= $fyear
                where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
                return $film
  let $count := count($films)
                
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};

declare function funcs:filmsOrderByAlfaPage($search, $page, $n) as element()*
{
   <root>
  {
  let $films := for $film in collection('Films')//movie
                order by $film/original-title
                where contains(fn:lower-case(data($film/original-title)), fn:lower-case($search))
                return $film
  let $count := count($films)
  for $film in subsequence($films, $page*$n+1, $n)
  return <elem>
          <count>{ $count }</count>
          <id>{ data($film/imdbid) }</id>
          <title>{ data($film/original-title) }</title>
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
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
          <cover>{ data($film/cover-url) }</cover>
          <rating>{ data($film/rating) }</rating>
          <votes>{ data($film/votes) }</votes>
          <actors>{
            subsequence( $film/cast//person/name , 0, 5)
          }
          </actors>
          <directors>{
          subsequence( $film/directors//name , 0, 3)
        }
          </directors>
          <year>{ $film/year/text() }</year>
          <genres>{ subsequence( $film/genres//item , 0, 9) }</genres>
                where contains($cat, data($genre))
         </elem>
  }
  </root>
};




declare function funcs:getFilm($id) as element()
 {
   let $film := collection('Films')/movies/movie[@id=$id]
   return $film
   
 };

declare updating function funcs:newFilm($path, $id)
{
    if (collection('Films')//movie[@id=$id]) then ()

    else (
    let $films := collection('Films')/movies
    let $new := doc($path)
    return insert node $new as last into $films
    )
};


 

