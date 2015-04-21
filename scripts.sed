s/([^()]*)//g
s/PW//g
/--\s/,$d 
/^[ \t]*>/d 
/^++/d 
/^--/d 
/^>/d  
/^+/d 
/^@/d 
/^#/d 
/^!/d 
/^To unsubscribe, e-mail:/d 
/^*/d 
/^[*/]/d 
/^-/d 
/^To contact the owner, e-mail:/d 
s/@[^@]*$// 
s!http[s]\?://\S*!!g 
s/^[0-9]{2}\/[A-Z][a-z]{2}\/[0-9]{4}//g 
s/PM//g 
s/AM//g 
s/^[0-9]\{1,2\}\/[0-9]\{1,2\}\/[0-9]\{4\}//g 
s/^[0-9]\{4\}\/[0-9]\{1,2\}\/[0-9]\{1,2\}//g 
s/[0-9]\{4\}\-[0-9]\{1,2\}\-[0-9]\{1,2\}//g 
s/[0-9]\{2\}\:[0-9]\{1,2\}\:[0-9]\{1,2\}//g 
s/\+[0-9]{4}//g 
s/\-[0-9]{4}//g 
s/[0-9]{4}\s[A-Z,a-z]{3}\s[0-9]{2}//g 
s/[0-9]{2}\s[A-Z,a-z]{3}\s[0-9]{4}//g 
/-----BEGIN PGP SIGNATURE-----/,/-----END PGP SIGNATURE-----/d 
/-----BEGIN PGP SIGNED MESSAGE-----/d 
/Hash: SHA1/d 
/GPG Fingerprint:/d 
/-----BEGIN PGP PUBLIC KEY BLOCK-----/,/-----END PGP PUBLIC KEY BLOCK-----/d 
/---/,/^$/d 
/^&&/d 
/^\[/d 
/^From:/d 
/^Date:/d 
/^Subject:/d 
/^Signed-off-by:/d 
/[0-9a-f]{7,40}/d  
/^Cc:/d 
                
