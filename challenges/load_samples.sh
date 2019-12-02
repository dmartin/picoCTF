#!/bin/bash

cd ./challenge-server
vagrant up
publish_output=`vagrant ssh -c "sudo shell_manager publish" shell`
docker exec pico_api python3 -c "import api
import json
with api.create_app().app_context():
  api.problem.load_published(json.loads(r\"\"\"$publish_output\"\"\"))
  for b in api.bundles.get_all_bundles():
      api.bundles.set_bundle_dependencies_enabled(b['bid'], True)"
