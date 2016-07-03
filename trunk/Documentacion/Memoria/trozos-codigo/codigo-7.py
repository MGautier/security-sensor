db_column = ['ID_Source_IP', 'ID_Dest_IP',
             'ID_Source_PORT', 'ID_Dest_PORT',
             'Protocol','ID_Source_MAC',
             'ID_Dest_MAC']

# El nombre de las tags, segun el orden de la
# columnas en db_column, las extraigo del fichero
# de configuracion a traves del registro info_config_file

labels = [self.info_config_file["Source_Ip"],
          self.info_config_file["Dest_Ip"],
          self.info_config_file["Source_Port"],
          self.info_config_file["Dest_Port"],
          self.info_config_file["Protocol"]]

# Almacenamos las etiquetas o campos del log de iptables
for it in tag_split:
    if len(it.split('=')) == 2:
        self.tag_log.append((it.split('='))[0].strip('\' '))

# Buscamos la correlacion entre los campos definidos en la
# configuracion con los extraidos del log de iptables

for label in labels:
    if (re.compile(label)).search(tag_str):
        if self.tag_log.index(label) > 0:
            db_column_name = db_column[0]
            register[db_column.pop(0)] = self.regexp(db_column_name, label, str(line))
            self.tag_log.remove(label)
    else:
        register[db_column.pop(0)] = None
