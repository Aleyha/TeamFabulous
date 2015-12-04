/etc/init.d/lighttpd restart
python main_program.py & echo $! >> run.pid
python line_detection.py & echo $! >> run.pid
python motor.py & echo $! >> run.pid
python server_backend.py & echo $! >> run.pid
