# #######################################################################################################################
#                                              # === LIBRAIRIES === #
# #######################################################################################################################
import pandas as pd
import hashlib
import numpy as np
import streamlit as st
import re
from datetime import datetime
import boto3
import s3fs

# #######################################################################################################################
#                                              # === FUNCTIONS === #
# #######################################################################################################################

# Création de l'empreinte SHA512 (128 caractères héxadécimaux)
def sha512_footprint_generation(firstname, lastname, dob, sex, salt):
    """..."""
    # Créé la chaine de caractères en entrée
    entry = (firstname+lastname+dob+sex+salt).encode('utf-8')
    # Transforme la chaine de caractères en 128 valeurs hexadecimales
    footprint = hashlib.sha512(entry).hexdigest()   
    return footprint


# Transformation de l'empreinte en nombres decimaux (deux caractères donnent un chiffre entre 0 et 255)
def hexadecimal_to_decical(footprint, size):
    """..."""
    decimal_nb = ""
    for iCharacter in np.arange(0, len(footprint), 2):
        doublet_hex = footprint[iCharacter:iCharacter+2]
        doublet_dec = str(int(doublet_hex, 16))
        decimal_nb += doublet_dec
    return decimal_nb[0:size]


# Création du nombre ID_PNMN sur la base du nom complet, du prénom complet, de la date de naissance, du genre et d'un sel.
def ID_PNMN_generator(firstname, lastname, dob, sex, salt, size):
    """..."""
    # Créé la valeur en hexadécimale
    footprint = sha512_footprint_generation(firstname, lastname, dob, sex, salt)
    # Transforme la valeur d'hexadecimale en décimale 
    ID_PNMN = hexadecimal_to_decical(footprint, size)
    return ID_PNMN

def convert_df(df):
    """..."""
    return df.to_csv(sep=';').encode('latin1')

# #######################################################################################################################
#                                              # === S3 AWS CONNEXION === #
# #######################################################################################################################

fs = s3fs.S3FileSystem(anon=False)
bucket_tables = "tables-de-comparaison"
bucket_repertoires = "repertoires-biopsies"


s3 = boto3.resource('s3')
my_bucket_img = s3.Bucket("tables-de-comparaison")
my_bucket_txt = s3.Bucket("repertoires-biopsies")

session = boto3.Session(
    aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY']
    )

# #######################################################################################################################
#                                              # === STREAMLIT === #
# #######################################################################################################################

