from beamngpy import BeamNGpy

#"C:\Users\rosem\AppData\Roaming\BeamMP-Launcher\BeamMP-Launcher.exe"

# beamng = BeamNGpy(
#     "localhost",
#     64256,
#     home=r"C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive",
#     user=r"C:\Users\rosem\Documents\BeamNG.drive"
# )

beamng = BeamNGpy(
    "localhost",
    64256,
    home=r"C:/Users/rosem/AppData/Roaming/BeamMP-Launcher/BeamMP-Launcher.exe",
    user=r"C:/Users/rosem/Documents/BeamNG.drive"
)

beamng.open()
print("Version BeamNG:", beamng.get_version())
beamng.close()
