
from threading import Thread
import cv2 as cv
import argparse
from multiprocessing import Process
from stella_bindings import stella_vslam

def run_viewer():
    global VIEWER
    VIEWER.run()

def run_localization_slam(map_db_path: str):     
    global SLAM
    global VIEWER
    # load configuration
    config = stella_vslam.config(config_file_path="./stella_bindings/config.yaml")
    # build a SLAM system
    SLAM = stella_vslam.system(cfg=config, vocab_file_path="./stella_bindings/orb_vocab.fbow")  
    # load the prebuilt map
    SLAM.load_map_database(map_db_path)
    # startup the SLAM process (it does not need initialization of a map)
    SLAM.startup(False)    

    # Extracted from example/run_camera_localization.cc of StellaVSLAM
    SLAM.disable_mapping_module()
    
    # create viewer object
    VIEWER = stella_vslam.viewer(config.yaml_node_['PangolinViewer'], SLAM)
    
    # run viewer in new thread to prevent GIL blocking
    viewerThread = Thread(target=run_viewer)
    viewerThread.start()
    key = cv.waitKey(1)
    if (key == 27):
        SLAM.shutdown()
        # stop viewer
        VIEWER.request_terminate()
        # wait for viewer thread to finish
        viewerThread.join()   

parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--vocab", help="vocabulary file path", default="./orb_vocab.dbow2")
# parser.add_argument("-c", "--config", help="config file path", default="./config.yaml")
parser.add_argument("-p", "--map_db", help="path to map file")
args = parser.parse_args()

p = Process(target=run_localization_slam, args=(args.map_db,)) 
p.start()
p.join()