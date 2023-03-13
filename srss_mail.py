#srss_mail.py

'''
ATTENTION !
1.- Vérifier que srss.dta soit présent
2.- si le script est repris dans crontab s'assurer que tout fichier mentionné dans le script le soit par son path complet!

'''
from time import time,localtime,gmtime
from yagmail import SMTP

def toEpoch(year,yearday): # prend les données directement ds le fichier srss.dta
    with open('/home/mib/Srss_Mail/srss.dta')as fi:
        epoch_sr_ss = 0 # temps epoch du lever et du coucher seront identiques jusqu'à yearday-1
        # Ajouter les secondes dans les années complètes écoulées depuis le 1er janvier 1970 à O heures
        for y in range(1970,year):
            epoch_sr_ss += 366*86400 if y%4==0 and y%100!=0 or y%400==0 else 365*86400
        # Ajouter les secondes des jours complets écoulés dans l'année en cours
        epoch_sr_ss += (yearday-1)*86400
        epoch_sr = epoch_ss = epoch_sr_ss # epoch_sr et epoch_ss se dissocient à partir d'ici
        for j in range(0,1463,4):
            l=[]
            for x in range(4):
                l.append(int(fi.readline()[:-1]))
            # l est ici 1 liste de 4 items : heures,minutes du lever puis du coucher, pour le jour courant 
            if j//4+1 == yearday: 
                # Ajouter les secondes et les minutes de l'heure du lever
                epoch_sr += l[0]*3600+l[1]*60
                # Ajouter les secondes et les minutes de l'heure du coucher
                epoch_ss += l[2]*3600+l[3]*60
                break # quitter la boucle "for j in range(0,1463,4):"
    return (epoch_sr,epoch_ss)

joursem=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']

# pas de wifi la nuit donc le mail sera envoyé la veille à 21h avec les données pour j+1
tomorrow=localtime(time()+86400)
nomjour=joursem[tomorrow[6]]
numjour=str(tomorrow[7])
sr_epoch=str(toEpoch(tomorrow[0],tomorrow[7])[0])
ss_epoch=str(toEpoch(tomorrow[0],tomorrow[7])[1])
jdhui=str(tomorrow[2])+"/"+str(tomorrow[1])+"/"+str(tomorrow[0])

lever=str(localtime(toEpoch(tomorrow[0],tomorrow[7])[0])[3])+":"+str(localtime(toEpoch(tomorrow[0],tomorrow[7])[0])[4])
coucher=str(localtime(toEpoch(tomorrow[0],tomorrow[7])[1])[3])+":"+str(localtime(toEpoch(tomorrow[0],tomorrow[7])[1])[4])
msgTosend=jdhui+' '+numjour+'  # '+lever+' '+coucher+' #  '+sr_epoch+' '+ss_epoch
print(msgTosend)

# Envoyer le mail 
SMTP("mibradoc@gmail.com", "hzmruwmsdcqruwrx").send("mibradoc@gmail.com",msgTosend,"Tout est dans le sujet")

