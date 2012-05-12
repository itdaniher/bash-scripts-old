if [ $1 = school ]
then
	LOC=chcaterm01
elif [ $1 = away ]
then
	LOC=204.10.217.225
fi
rdesktop \
-u ian.daniher -p 12345678 -K -r clipboard:CLIPBOARD -r disk:home=$HOME -g 1024x600 $LOC&
#See LICENSE file for copyright and license details
