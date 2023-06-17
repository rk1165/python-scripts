import time
import xml.etree.cElementTree as ET

name_space = {"xmlns:mes": "https://www.bea.com/WLS/JMS/Message"}

jms_message_export = ET.Element("JMSMessageExport")


def create_xml():
    jms_message = ET.SubElement(jms_message_export, 'mes:WLJMSMessage', name_space)
    header = ET.SubElement(jms_message, 'mes:Header')
    body = ET.SubElement(jms_message, 'mes:Body')
    body_string = "body"
    jms_message_id = "message_id"
    props = "<UDH>\n<H>\n<K>MESTYP</K>\n<V>SHPADV</V>\n</H>\n</UDH>\n"
    static_variable = "static var"

    ET.SubElement(header, 'mes:JMSMessageID').text = jms_message_id
    ET.SubElement(header, 'mes:JMSDeliveryMode').text = 'PERSISTENT'
    ET.SubElement(header, 'mes:JMSExpiration').text = str(round(time.time() * 1000) + 7 * 24 * 60 * 60 * 1000)
    ET.SubElement(header, 'mes:JMSPriority').text = '4'
    ET.SubElement(header, 'mes:JMSRedelivered').text = 'true'
    ET.SubElement(header, 'mes:JMSTimestamp').text = str(round(time.time() * 1000))
    properties = ET.SubElement(header, 'mes:Properties')

    udh = ET.fromstring(props)
    for header in udh.findall('H'):
        key = header.find('K').text
        value = header.find('V').text
        prop = ET.SubElement(properties, 'mes:property', name=key)
        if value is not None:
            ET.SubElement(prop, 'mes:String').text = value
        else:
            ET.SubElement(prop, 'mes:String').text = ''
    stat_var = ET.SubElement(properties, 'mes:property', name='StaticVariable')
    ET.SubElement(stat_var, 'mes:String').text = static_variable

    ET.SubElement(body, 'mes:Text').text = body_string
    print("Processed")


create_xml()

tree = ET.ElementTree(jms_message_export)
tree.write("sample.xml")
