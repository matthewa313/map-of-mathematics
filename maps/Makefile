# generate the map files directory for a given topic
cartographer $(TOPIC):
	mkdir -p $(TOPIC)
	cd $(TOPIC)
	mkdir $(TOPIC)/nodes
	mkdir $(TOPIC)/proofs
	touch $(TOPIC)/settings.json

# delete all jsons in all map subdirectories
clean:
	rm */nodes/network/*/*.json
	rm */nodes/network/*/*/*.json
	rm */nodes/network/*/*/*/*.json
	rm */nodes/network/*/*/*/*/*.json

# delete all svgs in all map subdirectories
# and write "{}" to */nodes/renders/.log.json
erase:
	rm */nodes/renders/*.svg
	echo "{}" > math/nodes/renders/.log.json
