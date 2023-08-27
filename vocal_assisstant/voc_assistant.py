import pyttsx3
import speech_recognition as sr
import pywhatkit as kit
import folium
import webbrowser
from pyroutelib3 import Router
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from numpy import sin, cos, arccos, pi, round
from datetime import timedelta
import geocoder

# Créer un objet de reconnaissance vocale
r = sr.Recognizer()

# Utilisation de Nominatim pour créer un géolocalisateur
geolocator = Nominatim(user_agent="user")

g = geocoder.ip('me')
my_lat = g.latlng[0]
my_long = g.latlng[1]

# Initialiser le moteur de synthèse vocale
engine = pyttsx3.init()

# Enregistrer un segment audio à partir du microphone

with sr.Microphone() as source:
        print("Parlez maintenant...")
        engine.say("Comment puis je t'aider")
        engine.runAndWait()
        audio = r.listen(source)

        # Transcrire le segment audio en texte
        try:
            texte = r.recognize_google(audio, language="fr-FR") # Changer la langue si besoin
            print("Vous avez dit : " + texte)

            #commande vocal
            if texte == 'météo':
                # Synthétiser le texte en audio
                print("Quelles villes ?")
                engine.say("Quelles villes ?")
                # Jouer le texte synthétisé
                engine.runAndWait()
                audio2 = r.listen(source)
                texte2 = r.recognize_google(audio2, language="fr-FR") # Changer la langue si besoin
                city_name = texte2
                print("voici les info météo à", city_name)
                # Synthétiser le texte en audio
                engine.say(f"voici les info météo à {city_name}")
                # Jouer le texte synthétisé
                engine.runAndWait()
                kit.search(f"météo {city_name}")

            elif texte == 'cherche sur Google':
                print("que dois je chercher ?")
                engine.say("que veux tu savoir ?")
                engine.runAndWait()
                audio2 = r.listen(source)
                texte2 = r.recognize_google(audio2, language="fr-FR") # Changer la langue si besoin
                google_search = texte2
                print("voici votre recherche :", google_search)
                engine.say(f"voici votre recherche : {google_search}")
                engine.runAndWait()
                kit.search(google_search)

            elif texte == 'vidéo':
                print("dites le nom de la vidéo ou bien de l'audio que vous voullez regarder/écouter...")
                engine.say("Que veux tu voir ou écouter ?")
                engine.runAndWait()
                audio2 = r.listen(source)
                texte2 = r.recognize_google(audio2, language="fr-FR") # Changer la langue si besoin
                média = texte2
                print("voici :"+ média)
                engine.say(f"voici : {média}")
                engine.runAndWait()
                kit.playonyt(média)
            
            elif texte == 'Maps':
                print("que veux tu savoir ?")
                engine.say("Que veux tu savoir ?")
                engine.runAndWait()
                audio2 = r.listen(source)
                texte2 = r.recognize_google(audio2, language="fr-FR") # Changer la langue si besoin
                maps = texte2
                if (maps=="ma position"):
                    print("vous avez dit : ",maps)
                    print('Voici une carte des lieux où nous sommes')
                    engine.say("Voici ta localisation")
                    engine.runAndWait()


                    m = folium.Map(location=[my_lat,my_long], zoom_start=150)

                    folium.Marker(
                    location=[my_lat,my_long],
                    popup = 'Me',  # Texte du popup
                    icon=folium.Icon(color="yellow"),
                    ).add_to(m)

                    m.save('m.html')
                    webbrowser.open('m.html')

                elif texte == "exit":
                    exit()

                elif maps =="itinéraire":
                    print("Quelle est le lieu de départ ?")
                    engine.say("Quelle est le lieu de départ ?")
                    engine.runAndWait()
                    audio2 = r.listen(source)
                    texte3 = r.recognize_google(audio2, language="fr-FR") # Changer la langue si besoin
                    print(texte3)
                    # Obtenir les coordonnées GPS des lieux de départ et d'arrivée
                    q1 = texte3
                    print("Quelle est le lieu d'arrivée ?")
                    engine.say("Quelle est le lieu d'arrivée ?")
                    engine.runAndWait()
                    audio2 = r.listen(source)
                    texte4 = r.recognize_google(audio2, language="fr-FR") # Changer la langue si besoin
                    print(texte4)
                    # Obtenir les coordonnées GPS des lieux de départ et d'arrivée
                    q2 = texte4

                   # Dictionnaires de mapping
                    transport_fr_en = {
                    "à vélo":"cycle",
                    "à pied":"foot",
                    "à cheval":"horse", 
                    "en tramway":"tram",
                    "en train":"train",
                    "en voiture":"car"
                    }

                    transport_speeds = {
                    "à vélo": 24,
                    "à pied": 4.7,
                    "à cheval": 10, 
                    "en tramway": 20,
                    "en train": 50,
                    "en voiture": 51.3
                    }

                    # Créer une instance de Router avec le moyen de transport spécifié
                    print("Quel moyen de transport utilisez-vous (cycle, foot, horse, tram, train, car) ? : ")
                    engine.say("comment vous vous déplacer")
                    engine.runAndWait()
                    audio2 = r.listen(source)
                    texte5 = r.recognize_google(audio2, language="fr-FR") # Changer la langue si besoin
                    transport_fr = texte5
                  # Validation
                    if transport_fr in transport_fr_en:

                        # Traduire 
                        transport_en = transport_fr_en[transport_fr]

                        print(f"Trajet {transport_fr} calculé")
                        engine.say(f"Trajet {transport_fr} calculé")
                        engine.runAndWait()

                        # Récupérer vitesse
                        speed = transport_speeds[transport_fr]

                        # Instancier le routeur 
                        router = Router(transport_en)

                    else:
                        print("Transport invalide")
                        engine.say("Transport invalide.")
                        engine.runAndWait()
                        

                    location_start = geolocator.geocode(q1)
                    start = [location_start.latitude, location_start.longitude]

                    location_end = geolocator.geocode(q2)
                    end = [location_end.latitude, location_end.longitude]

                    # Calcul de la distance à partir de coordonnées
                    def rad2deg(radians):
                        degrees = radians * 180 / pi
                        return degrees

                    def deg2rad(degrees):
                        radians = degrees * pi / 180
                        return radians

                    def getDistanceBetweenPointsNew(unit='kilometers'):
                        theta = start[1] - end[1]
                        distance = 60 * 1.1515 * rad2deg(
                            arccos(
                                (sin(deg2rad(start[0])) * sin(deg2rad(end[0]))) +
                                (cos(deg2rad(start[0])) * cos(deg2rad(end[0])) * cos(deg2rad(theta)))
                            )
                        )
                        
                        if unit == 'miles':
                            return round(distance, 2)
                        if unit == 'kilometers':
                            return round(distance * 1.609344, 2)
                            
                    distance_km = getDistanceBetweenPointsNew('kilometers')
                    distance_miles = getDistanceBetweenPointsNew('miles')

                    print(f"Distance en kilomètres : {distance_km} km")
                    engine.say(f"Distance en kilomètres : {distance_km} km")
                    engine.runAndWait()
                    print(f"Distance en miles : {distance_miles} miles")

                    # Estimation de la durée du trajet
                    # Récupérer la vitesse du transport choisi 

                    # Faire la division avec la valeur speed
                    travel_time = distance_km / speed


                    # Convertir la durée en heures et minutes
                    travel_hours = int(travel_time)
                    travel_minutes = int((travel_time - travel_hours) * 60)

                    print(f"La durée du trajet est d'environ : {travel_hours} heures {travel_minutes} minutes")
                    engine.say(f"La durée du trajet est d'environ : {travel_hours} heures {travel_minutes} minutes")
                    engine.runAndWait()


                    # Trouver les nœuds de départ et d'arrivée les plus proches
                    depart = router.findNode(start[0], start[1])
                    arrivee = router.findNode(end[0], end[1])

                    # Calculer l'itinéraire : tester l'existence d'une route
                    status, itineraire = router.doRoute(depart, arrivee)

                    if status == 'success':
                        engine.say("voici votre trajet")
                        engine.runAndWait()
                        routeLatLons = list(map(router.nodeLatLon, itineraire))  # Liste des points du parcours

                        # Créer une carte
                        carte = folium.Map(location=[(start[0] + end[0]) / 2, (start[1] + end[1]) / 2], zoom_start=15)

                        # Calcul de la distance totale
                        total_distance = 0

                        # Ajouter des points (noeuds) du parcours à la carte
                        for i in range(1, len(routeLatLons)):
                            prev_node = routeLatLons[i - 1]
                            node = routeLatLons[i]

                            # Calcul de la distance entre les nœuds
                            dist = geodesic(prev_node, node).km

                            # Mise à jour de la distance totale
                            total_distance += dist
                            

                            # Ajouter un marqueur à la carte tous les 500 mètres
                            if total_distance >= 0.5:
                                
                                folium.Marker(location=node).add_to(carte)
                                total_distance = 0

                        # Ajouter à la carte le tracé d'une ligne reliant les points/noeuds du parcours
                        folium.PolyLine(routeLatLons, color="blue", weight=2.5, opacity=1, popup=(f"durée estimée :{travel_hours} heures {travel_minutes} minutes")).add_to(carte)

                        # Ajouter des marqueurs pour les points de départ et d'arrivée
                        folium.Marker(
                            location=[end[0], end[1]],
                            popup=location_end.address,
                            icon=folium.Icon(color="red")
                        ).add_to(carte)

                        folium.Marker(
                            location=[start[0], start[1]],
                            popup=location_start.address,
                            icon=folium.Icon(color="green")
                        ).add_to(carte)

                        # Enregistrement et affichage de la carte
                        carte.save('carte.html')
                        webbrowser.open('carte.html')
                    else:
                        print("Impossible de trouver un itinéraire pour ce moyen de transport.")
                        engine.say("Impossible de trouver un itinéraire pour ce moyen de transport.")
                        engine.runAndWait()

                else:
                    print("Je n'ai pas compris votre commande. Pouvez-vous répéter ?")
                    engine.say("Je n'ai pas compris votre commande. Pouvez-vous répéter ?")
                    engine.runAndWait()
            else:
                print("Je n'ai pas compris votre commande. Pouvez-vous répéter ?")
                engine.say("Je n'ai pas compris votre commande. Pouvez-vous répéter ?")
                engine.runAndWait()

        except sr.UnknownValueError:
            print("Je n'ai pas compris.")
            texte = "je n'ai pas compris"
        except sr.RequestError as e:
            print("Erreur lors de la requête : {0}".format(e))
            texte = "Erreur lors de la requête : {0}"
