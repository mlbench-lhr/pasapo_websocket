# websocket/funcs/mongo_listener.py - DEBUG VERSION
import threading
import pymongo
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .common_funcs import *

def watch_properties():
    try:
        client = pymongo.MongoClient(
            "mongodb://admin:mlbprivate321@213.159.6.36:27017/admin?replicaSet=rs0",
            serverSelectionTimeoutMS=5000  # 5 second timeout
        )
        
        client.admin.command('ping')
        
        db = client["pasapo"]
        collection = db["properties"]
        
        with collection.watch() as stream:
            
            for change in stream:
                op_type = change["operationType"]
                _id = change["documentKey"]["_id"]

                # Case 1: insert or replace
                if op_type in ("insert", "replace"):
                    doc = collection.find_one({"_id": _id})
                    
                    if doc:
                        has_kbs = doc.get("kbs_socket_info") is not None
                        has_id = doc.get("id") is not None
                        
                        if has_kbs and has_id:
                            property_id = str(doc['id'])
                            group_name = f"property_{property_id}"
                            
                            try:
                                channel_layer = get_channel_layer()
                                async_to_sync(channel_layer.group_send)(
                                    group_name,
                                    {
                                        "type": "property_update",
                                        "kbs_socket_info": doc["kbs_socket_info"],
                                    }
                                )
                            except Exception as e:
                                logger.debug(f"❌ Error broadcasting: {e}")
                        else:
                            logger.debug("⚠️ Document missing required fields, skipping...")
                    else:
                        logger.debug("❌ Document not found after insert/replace")

                # Case 2: update
                elif op_type == "update":
                    updated_fields = change["updateDescription"]["updatedFields"]
                    if "kbs_socket_info" in updated_fields:
                        doc = collection.find_one({"_id": _id})
                        
                        if doc:
                            has_kbs = doc.get("kbs_socket_info") is not None
                            has_id = doc.get("id") is not None
                            if has_kbs and has_id:
                                property_id = str(doc['id'])
                                group_name = f"property_{property_id}"
                                
                                try:
                                    channel_layer = get_channel_layer()
                                    async_to_sync(channel_layer.group_send)(
                                        group_name, doc["kbs_socket_info"]
                                    )
                                except Exception as e:
                                    logger.debug(f"❌ Error broadcasting: {e}")
                            else:
                                logger.debug("⚠️ Document missing required fields, skipping...")
                        else:
                            logger.debug("❌ Document not found after update")
                    else:
                        logger.debug("ℹ️ kbs_socket_info not in updated fields, ignoring...")
                
                else:
                    logger.debug(f"ℹ️ Ignoring operation type: {op_type}")
                    
    except Exception as e:
        logger.debug(f"❌ Error in watch_properties: {e}")
        import traceback
        traceback.logger.debug_exc()

def start_mongo_listener():
    
    try:
        thread = threading.Thread(target=watch_properties, daemon=True, name="MongoDB-Listener")
        thread.start()
        
    except Exception as e:
        logger.debug(f"❌ Error starting thread: {e}")
        import traceback
        traceback.logger.debug_exc()