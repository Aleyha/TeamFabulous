/etc/init.d/lighttpd restart
python /home/fart/TeamFabulous/comms/main_program.py & echo $! >> run.pid
python /home/fart/TeamFabulous/lineDetection/line-detection.py & echo $! >> run.pid
python /home/fart/TeamFabulous/comms/motor.py & echo $! >> run.pid
#testing only
#python server_backend.py & echo $! >> run.pid
