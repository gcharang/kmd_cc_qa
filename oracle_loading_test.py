#!/usr/bin/env python3
import json
from subprocess import check_output
from test_modules import file_oraclize

ac_name = input("Input AC name with which you want to work (exmp: ORCL): ")
oracles_number = int(input("Input how many oracles do you want to create: "))
oracles_type = input("Set your oracle type (e.g. d): ")

def oracle_create(ac_name, name, description, type):
    new_oracle = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"oraclescreate",name,description,type]))
    byte_oracle_id = check_output(
    ["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_oracle["hex"]])
    oracle_id = byte_oracle_id.decode().rstrip()

    return oracle_id

def oracle_register(ac_name, oracle_id, datafee):
    new_registration = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"oraclesregister",oracle_id,datafee]))
    byte_registration_id = check_output(
    ["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_registration["hex"]])
    batontx_id = byte_registration_id.decode().rstrip()

    return batontx_id

def oracle_subscribe(ac_name, oracle_id, publisher_id, datafee):
    new_subscription = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"oraclessubscribe",oracle_id,publisher_id,datafee]))
    byte_subscription_id = check_output(
    ["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_subscription["hex"]])
    subscription_txid = byte_subscription_id.decode().rstrip()

    return subscription_txid

file1 = open("oracles_list", "w")
while oracles_number > 0:
    new_oracle = oracle_create(ac_name, "test", "test", oracles_type)
    file1.writelines(new_oracle + "\n")
    oracles_number = oracles_number - 1
file1.close()
print("Oracles succesfully created. IDs can be found in oracles_list file")

file = open("oracles_list", "r")
file2 = open("register_list", "w")
for line in file:
    new_registration = oracle_register(ac_name, line, "100000")
    print(new_registration)
    file2.writelines(new_registration + "\n")
file2.close()
file.close()
print("Oracles registration txs broadcasted. Baton TX IDs can be found in register_list file")

file = open("oracles_list", "r")
file3 = open("register_list", "r")
file4 = open("subscriptions_list", "w")
for line1, line2 in zip(file, file3):
    new_subscription = oracle_subscribe(ac_name, line1, line2, "10000")
    print(new_subscription)
    file4.writelines(new_subscription + "\n")
file4.close()
print("Oracles subscribtion txs broadcasted. Subscription TX IDs can be found in subscriptions_list file")

# subscribe on all oracles

# checking if subscribed on all oracles

# print("Preparation done. Ready to publish the data")

# choosing file to publish

#2) run concurent data uploading to X oracles
#3) grab data from X oracles
#4) compare data for X files
