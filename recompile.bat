cd /d "C:\Users\Utilisateur\Documents\entitylib2-master"
mkdir dist
robocopy textures dist\textures
robocopy textures\letter dist\textures\letter
robocopy textures\letters dist\textures\letters
robocopy textures\effect dist\textures\effect
robocopy image dist\image
robocopy images dist\images
robocopy map dist\map
robocopy sounds dist\sounds
copy map.txt dist
copy minimap.txt dist
py -3.4 -m py2exe.build_exe "C:\Users\Utilisateur\Documents\entitylib2-master\main.py" "C:\Users\Utilisateur\Documents\entitylib2-master\entitylib2.py"