import threading
import pymongo
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .common_funcs import *

def watch_properties():
    try:
        with properties_col.watch() as stream:
            
            for change in stream:
                op_type = change["operationType"]
                _id = change["documentKey"]["_id"]

                # Case 1: insert or replace
                if op_type in ("insert", "replace"):
                    doc = properties_col.find_one({"_id": _id})
                    
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
                                logger.debug(f"❌ Error broadcasting property: {e}")
                        else:
                            logger.debug("⚠️ Property document missing required fields, skipping...")
                    else:
                        logger.debug("❌ Property document not found after insert/replace")

                # Case 2: update
                elif op_type == "update":
                    updated_fields = change["updateDescription"]["updatedFields"]
                    if "kbs_socket_info" in updated_fields:
                        doc = properties_col.find_one({"_id": _id})
                        
                        if doc:
                            has_kbs = doc.get("kbs_socket_info") is not None
                            has_id = doc.get("id") is not None
                            if has_kbs and has_id:
                                property_id = str(doc['id'])
                                group_name = f"property_{property_id}"
                                
                                try:
                                    channel_layer = get_channel_layer()
                                    async_to_sync(channel_layer.group_send)(
                                        group_name,{
                                        "type": "property_update",
                                        "kbs_socket_info": doc["kbs_socket_info"],
                                    }
                                    )
                                except Exception as e:
                                    logger.debug(f"❌ Error broadcasting property: {e}")
                            else:
                                logger.debug("⚠️ Property document missing required fields, skipping...")
                        else:
                            logger.debug("❌ Property document not found after update")
                    else:
                        logger.debug("ℹ️ kbs_socket_info not in updated fields for property, ignoring...")
                
                else:
                    logger.debug(f"ℹ️ Ignoring property operation type: {op_type}")
                    
    except Exception as e:
        logger.debug(f"❌ Error in watch_properties: {e}")
        


def watch_guests():
    try:
        with guests_col.watch() as stream:
            
            for change in stream:
                op_type = change["operationType"]
                _id = change["documentKey"]["_id"]

                # Case 1: insert or replace
                if op_type in ("insert", "replace"):
                    doc = guests_col.find_one({"_id": _id})
                    
                    if doc:
                        has_kbs = doc.get("kbs_socket_info") is not None
                        has_id = doc.get("id") is not None
                        
                        if has_kbs and has_id:
                            guest_id = str(doc['id'])
                            group_name = f"guest_{guest_id}"
                            
                            try:
                                channel_layer = get_channel_layer()
                                async_to_sync(channel_layer.group_send)(
                                    group_name,
                                    {
                                        "type": "guest_update",
                                        "kbs_socket_info": doc["kbs_socket_info"],
                                    }
                                )
                            except Exception as e:
                                logger.debug(f"❌ Error broadcasting guest: {e}")
                        else:
                            logger.debug(f"⚠️ Guest document missing required fields - has_kbs: {has_kbs}, has_id: {has_id}")
                    else:
                        logger.debug(f"❌ Guest document not found after {op_type}")

                # Case 2: update
                elif op_type == "update":
                    updated_fields = change["updateDescription"]["updatedFields"]
                    
                    if "kbs_socket_info" in updated_fields:
                        doc = guests_col.find_one({"_id": _id})
                        
                        if doc:
                            has_kbs = doc.get("kbs_socket_info") is not None
                            has_id = doc.get("id") is not None
                            
                            if has_kbs and has_id:
                                guest_id = str(doc['id'])
                                group_name = f"guest_{guest_id}"
                                
                                try:
                                    channel_layer = get_channel_layer()
                                    async_to_sync(channel_layer.group_send)(
                                        group_name,{
                                        "type": "guest_update",
                                        "kbs_socket_info": doc["kbs_socket_info"],
                                    }
                                    )
                                except Exception as e:
                                    logger.debug(f"❌ Error broadcasting guest: {e}")
                            else:
                                logger.debug(f"⚠️ Guest document missing required fields - has_kbs: {has_kbs}, has_id: {has_id}")
                        else:
                            logger.debug("❌ Guest document not found after update")
                    else:
                        logger.debug("ℹ️ kbs_socket_info not in updated fields for guest, ignoring...")
                
                else:
                    logger.debug(f"ℹ️ Ignoring guest operation type: {op_type}")
                    
    except Exception as e:
        logger.debug(f"❌ Error in watch_guests: {e}")
        


def start_mongo_listener():
    try:
        # Start property watcher thread
        property_thread = threading.Thread(target=watch_properties, daemon=True, name="MongoDB-Property-Listener")
        property_thread.start()
        logger.debug("🚀 Started MongoDB Property Listener")
        
        # Start guest watcher thread
        guest_thread = threading.Thread(target=watch_guests, daemon=True, name="MongoDB-Guest-Listener")
        guest_thread.start()
        logger.debug("🚀 Started MongoDB Guest Listener")
        
    except Exception as e:
        logger.debug(f"❌ Error starting threads: {e}")
        