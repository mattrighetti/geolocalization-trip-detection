import requests
import pymongo

class MongoDBManager(object):

    def __init__(self):
        # Get cluster
        self.client = pymongo.MongoClient(
            "mongodb+srv://python-microservice:J5MTvCIJMb5TcM5S@geolocalization-izvf1.mongodb.net/test?retryWrites=true&w=majority")
        # Get database
        self.db = client.get_database('backend')
        # Get collection
        self.trip_records = db.trips

    def save_to_database_args(self, user_id=None, ticket_id=None,
                              km_travelled=None, transportation=None, start_time=None, end_time=None):
        """
        This method will let users save a document to a remote MongoDB by providing every single argument
        param data_dict: dictionary of user data to be saved
        @param user_id: User ID
        @param ticket_id: Ticket ID
        @param km_travelled: Km travelled by the user
        @param transportation: Mean of transportation predicted
        @param start_time: Trip start time
        @param end_time: Trip end time
        """

        if user_id is None or \
                ticket_id is None or \
                km_travelled is None or \
                transportation is None or \
                start_time is None or \
                end_time is None:

            raise Exception("Missing data")

        # Create new data
        data = {
            'user_id' : user_id,
            'ticket_id' : ticket_id,
            'km_travelled' : km_travelled,
            'transportation' : transportation,
            'start_time' : start_time,
            'end_time' : end_time
        }

        print(f'Saving data_dict{data} to MongoDB...')
        self.trip_records.insert_one(data)
        print(f'Saved successfully!')

    def save_to_database_dict(self, data_dict):
        """
        This method will let users save a dictionary without providing every single argument as a function arg
        @param data_dict: dictionary of user data to be saved
        @param data_dict:
        """
        necessary_data = ('user_id', 'ticket_id', 'transportation', 'start_time', 'end_time')
        if not all(key in data_dict for key in necessary_data):
            raise Exception("Dictionary has incorrect keys")
        else:
            print(f'Saving data_dict{data_dict} to MongoDB...')
            self.trip_records.insert_one(data_dict)
            print(f'Saved successfully!')