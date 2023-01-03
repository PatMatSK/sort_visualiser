cat main.py | tail -r | tail -n +2 | tail -r > tmp.py
mv tmp.py main.py
python3 test_sorting.py
echo "root.mainloop()" >> main.py
