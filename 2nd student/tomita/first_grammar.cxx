#encoding "utf-8"

Main -> S;
Name -> Word<kwtype="Имя"> ;
Thing -> Word<kwtype="Штука"> ;

//ThingD -> Thing interp (Culture.Thing);
//NameD -> Name interp (Culture.Name);
S -> Name interp (Culture.Name);
S -> Thing interp (Culture.Thing);

