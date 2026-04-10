from flask import Flask,request,jsonify,send_from_directory
app=Flask(__name__)
import pandas as pd

df=pd.read_csv("/Users/snehasharma/Documents/AGENTIC AI WORKSHOP/flights.csv")


# arr_delay,dep_delay ,dep_time  ,arr_time,tailnum ,air_time

df=df.drop(['air_time','tailnum'],axis=1)

df['dep_time'].fillna(df['dep_time'].median(), inplace=True)
df['arr_time'].fillna(df['arr_time'].median(), inplace=True)
df['dep_delay'].fillna(df['dep_delay'].median(), inplace=True)
df['arr_delay'].fillna(df['arr_delay'].median(), inplace=True)
# print(df.isnull().sum())

booking_data={}
def get_response(user_input):
    # print("Chatbot: Hi!I'm your simple chatbot.\n I am here to help u regarding flight bookings ")
    # print()

    # while(True):
        # user_input=input("You: ").lower()
        
        user_input=user_input.lower()
        if "bye" in user_input:
            return " Goodbye!! have a nice day 😊"
            # break
        elif "hello" in user_input or "hii" in user_input or "hey" in user_input:
            return " Hello how can i help you??"
            
        elif "help" in user_input:
            return " Yes I cen help for sure!!"
            
        # q-1 Which flights have the longest dep_delay or arr_delay?++
        elif "longest" in user_input and ("departure delay" in user_input or "arrival delay" in user_input):
                if "departure delay" in user_input :
                    
                    idx=df['dep_delay'].idxmax()
                    result=str(df.loc[idx, 'carrier']) + str(df.loc[idx, 'flight'])
                    return " this flight number  :" +result
                    
                if "arrival delay" in user_input :
                   
                    idx=df['arr_delay'].idxmax()
                    result=str(df.loc[idx, 'carrier']) + str(df.loc[idx, 'flight'])
                    return " this flight number :"+result 
                    
# q-Which flights leave the earliest in the morning
        elif "earliest" in user_input and "morning" in user_input :
             idx=df['dep_time'].idxmin()
             result =str(df.loc[idx, 'carrier']) + str(df.loc[idx, 'flight'])+" " +str(df.loc[idx, 'name']) 
             return " this flight number :" +result 
            
# q-Which airline has the highest percentage of on-time departures 
        elif "on time" in user_input and "departure" in user_input:
             idx=df['dep_delay'].idxmin()
             result =str(df.loc[idx, 'carrier']) + str(df.loc[idx, 'flight'])+" " +str(df.loc[idx, 'name']) 
             return " this flight number :" +result
        
        

        elif "book"  in user_input and  "tickets" in user_input:
            booking_data.clear()
            return "Yess sure!!. Enter from where u want to travel??"
        
        elif "from" in user_input:
             booking_data['source'] = user_input.split("from")[-1].strip()
             return "To where??"
        elif "to" in user_input:
             booking_data['destination'] = user_input.split("to")[-1].strip()
             return "OK GREAT ! \n Now enter travel date "
        elif "202" in user_input:
             booking_data['date'] = user_input
             return "How many passengers?"
        elif user_input.isdigit():
             booking_data['passengers'] = int(user_input)
             return f"""
Booking Summary:
From: {booking_data.get('source')}
To: {booking_data.get('destination')}
Date: {booking_data.get('date')}
Passengers: {booking_data.get('passengers')}

Type 'confirm' to proceed.
Type 'cancel' to cancel tickets
"""
        elif "confirm" in user_input:
             return " Yayy!! Tickets are ready to be booked "
        
        elif "cancel" in user_input:
             booking_data.clear()
             return "Tickets Cancelled Now ❌"
        
        
        else:
          return "Chatbot: Sorry ! i could not understand your question. \n check if u have any mistake in the question "
            
        

app = Flask(__name__, static_folder='images', static_url_path='/images')


@app.route("/")
def home():
     return send_from_directory('.','forms.html')

@app.route("/chat",methods=["POST"])

 
def chat():
     data=request.json
     user_input=data.get("message")
     response = get_response(user_input)
     return jsonify({"response":response})

if __name__=="__main__":
     print("chatbot is running ! Visit http://127.0.0.1:5000 in your browser")
     print("serving forms.html file")
     app.run(debug=True)
