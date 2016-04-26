file="run.pid"
while read line
do
	echo $line
	kill $line
rm run.pid
done < "$file"
