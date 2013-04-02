#!/bin/sh

cat ~/.walloptrc
diff ~/.walloptrc ~/.walloptrc_
if [ $? -eq 0 ] ; then
	echo 'equall'
else
	echo 'difference'
fi

echo 'b backup'
echo 'r recover'
echo 'e edit'
echo 'n no'
echo '(b|r|e|n)'
read YN

if [ $YN = 'b' ] ; then
	cp ~/.walloptrc ~/.walloptrc_
elif [ $YN = 'r' ] ; then
	cp ~/.walloptrc_ ~/.walloptrc
elif [ $YN = 'e' ] ; then
	vi ~/.walloptrc
elif [ $YN = 'n' ] ; then
	echo 'no change.'
else
	echo 'expected b | r | e | n'
	exit 1
fi

cat ~/.walloptrc

exit 0
