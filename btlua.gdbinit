define btlua
	set $p = L.ci
	while ($p != 0 )
		set $tt = ($p.func.tt_ & 0x3f)
		if ( $tt == 0x06 )
		set $proto = $p.func.value_.gc.cl.l.p
		 set $filename = ( char *) (&( $proto.source.tsv ) + 1)
		 set $lineno = $proto.lineinfo[ $p.u.l.savedpc - $proto.code -1 ]
		 printf "0x%x LUA FUNCTION : %4d %s\n", $p , $lineno , $filename
		
		 set $p = $p.previous
		 loop_continue
		 end
		
		 if ( $tt == 0x16 )
		 printf "0x%x LIGHT C FUNCTION ", $p
		 output $p.func.value_.f
		 printf "\n"
		
		 set $p = $p.previous
		 loop_continue
		 end
		
		 if ( $tt == 0x26 )
		 printf "0x%x C FUNCTION ", $p
		 output $p.func.value_.gc.cl.c.f
		 printf "\n"
		
		 set $p = $p.previous
		 loop_continue
		 end
		
		 printf "0x%x LUA BASE \n", $p
		 set $p = $p.previous
		 end
