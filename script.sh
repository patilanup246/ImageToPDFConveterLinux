#!\bin\bash
{
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR	
LICZ=0
ext='.pdf'
mkdir buff
folder="./buff/"
LIST=''
TMP="tmp"
	function save {
		
		echo "folder z danymi: $1"

while IFS=$'\t' read -r COLONE COLTWO COLTHREE COLFOUR
do
	echo "$COLONE"
	x=$(echo $COLONE | sed "s/.*\.//")
	LICZ=$(($LICZ+1))
	if [[ "$x" == "doc" ]] ; then
		DOCEXT='.doc'
		cp $COLONE $folder$LICZ$DOCEXT
		libreoffice --headless --convert-to pdf $folder$LICZ$DOCEXT
		mv $LICZ$ext $folder$LICZ$ext
		echo "25"
	elif [[ "$x" == "pdf" ]] ; then
		cp $COLONE $folder$LICZ$ext
 	elif [[ ( "$x" == "jpg" ) || ( "$x" == "png" ) ]] ; then
		convert $COLONE $folder$LICZ$ext
	else		
		echo "poczatek"
		find $COLONE | grep '\.[a-z][a-z][a-z]' > buff12.txt
		tac buff12.txt > buff1.txt
		save buff1.txt
		echo "koniec"
		continue
	fi
	LIST="${LIST} ${folder}${LICZ}${ext}"
	
	if [[ ( "$x" == "pdf" ) || ( "$x" == "doc" ) ]] ; then
		if [[ "$COLFOUR" == "999" || "$COLFOUR" == "" ]] ; then
			COLFOUR="end"
		fi
		if [[ ( "$COLTHREE" == "" ) || ( "$COLTHREE" == "0" )  ]] ; then
			COLTHREE=1
		fi
		
		pdftk $folder$LICZ$ext cat $COLTHREE-$COLFOUR output $folder$LICZ$TMP$ext
		cp $folder$LICZ$TMP$ext $folder$LICZ$ext
		rm -r $folder$LICZ$TMP$ext
	fi
	
	if [[ $COLTWO ]] ; then
		convert $folder$LICZ$ext -rotate -$COLTWO $folder$LICZ$ext
	fi

done <<< "$(cat $1)"

}

save data.txt
echo "lista plikow: $LIST"
pdftk $LIST cat output $1
echo "Folder docelowy: $1"
rm -r buff


}
