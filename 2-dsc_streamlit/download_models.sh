#!/bin/bash

BASE_URL="https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/"

mkdir -p streamlit/models/

curl -o streamlit/models/candy.t7 "$BASE_URL/instance_norm/candy.t7"
curl -o streamlit/models/la_muse.t7 "$BASE_URL/instance_norm/la_muse.t7"
curl -o streamlit/models/mosaic.t7 "$BASE_URL/instance_norm/mosaic.t7"
curl -o streamlit/models/feathers.t7 "$BASE_URL/instance_norm/feathers.t7"
curl -o streamlit/models/the_scream.t7 "$BASE_URL/instance_norm/the_scream.t7"
curl -o streamlit/models/udnie.t7 "$BASE_URL/instance_norm/udnie.t7"
curl -o streamlit/models/the_wave.t7 "$BASE_URL/eccv16/the_wave.t7"
curl -o streamlit/models/starry_night.t7 "$BASE_URL/eccv16/starry_night.t7"
curl -o streamlit/models/la_muse_eccv16.t7 "$BASE_URL/eccv16/la_muse.t7"
curl -o streamlit/models/composition_vii.t7 "$BASE_URL/eccv16/composition_vii.t7"