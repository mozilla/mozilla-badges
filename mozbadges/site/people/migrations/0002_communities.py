# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def get_communities(self):
        return (
            ('ARABIC', 'Arabic', 'arabic', '6_OTHER'),
            ('BALKANS', 'Balkans', 'balkans', '6_OTHER'),
            ('FRANCOPHONE', 'Francophone', 'francophone', '6_OTHER'),
            ('HISPANO', 'Hispano', 'hispano', '6_OTHER'),

            ('AL', 'Albania', 'albania', '3_EUR'),
            ('DZ', 'Algeria', 'algeria', '5_A_ME'),
            ('AQ', 'Antarctica', 'antarctica', '6_OTHER'),
            ('AR', 'Argentina', 'argentina', '2_LAT_AM'),
            ('AM', 'Armenia', 'armenia', '3_EUR'),
            ('AU', 'Australia', 'australia', '4_ASIA_SP'),
            ('AT', 'Austria', 'austria', '3_EUR'),
            ('BD', 'Bangladesh', 'bangladesh', '4_ASIA_SP'),
            ('ES_PV', 'Basque', 'basque', '3_EUR'),
            ('BE', 'Belgium', 'belgium', '3_EUR'),
            ('BO', 'Bolivia', 'bolivia', '2_LAT_AM'),
            ('BA', 'Bosnia and Herzegovina', 'bosnia-and-herzegovina', '3_EUR'),
            ('BR', 'Brazil', 'brazil', '2_LAT_AM'),
            ('BG', 'Bulgaria', 'bulgaria', '3_EUR'),
            ('KH', 'Cambodia', 'cambodia', '4_ASIA_SP'),
            ('CA', 'Canada', 'canada', 'US_CAN'),
            ('CT', 'Catalan', 'catalan', '3_EUR'),
            ('CL', 'Chile', 'chile', '2_LAT_AM'),
            ('CN', 'China', 'china', '4_ASIA_SP'),
            ('CO', 'Colombia', 'colombia', '2_LAT_AM'),
            ('CR', 'Costa Rica', 'costa-rica', '2_LAT_AM'),
            ('HR', 'Croatia', 'croatia', '3_EUR'),
            ('CU', 'Cuba', 'cuba', '2_LAT_AM'),
            ('CZ', 'Czech Republic', 'czech-republic', '3_EUR'),
            ('DK', 'Denmark', 'denmark', '3_EUR'),
            ('EC', 'Ecuador', 'ecuador', '2_LAT_AM'),
            ('EG', 'Egypt', 'egypt', '5_A_ME'),
            ('FI', 'Finland', 'finland', '3_EUR'),
            ('FR', 'France', 'france', '3_EUR'),
            ('DE', 'Germany', 'germany', '3_EUR'),
            ('GH', 'Ghana', 'ghana', '5_A_ME'),
            ('GR', 'Greece', 'greece', '3_EUR'),
            ('HK', 'Hong Kong', 'hong-kong', '4_ASIA_SP'),
            ('HU', 'Hungary', 'hungary', '3_EUR'),
            ('IN', 'India', 'india', '4_ASIA_SP'),
            ('ID', 'Indonesia', 'indonesia', '4_ASIA_SP'),
            ('IE', 'Ireland', 'ireland', '3_EUR'),
            ('IL', 'Israel', 'israel', '5_A_ME'),
            ('IT', 'Italy', 'italy', '3_EUR'),
            ('CI', 'Ivory Coast', 'ivory-coast', '5_A_ME'),
            ('JP', 'Japan', 'japan', '4_ASIA_SP'),
            ('JO', 'Jordan', 'jordan', '5_A_ME'),
            ('KE', 'Kenya', 'kenya', '5_A_ME'),
            ('IN_KL', 'Kerala', 'kerala', '4_ASIA_SP'),
            ('XK', 'Kosovo', 'kosovo', '3_EUR'),
            ('LT', 'Lithuania', 'lithuania', '3_EUR'),
            ('MK', 'Macedonia', 'macedonia', '3_EUR'),
            ('MY', 'Malaysia', 'malaysia', '4_ASIA_SP'),
            ('MU', 'Mauritius', 'mauritius', '5_A_ME'),
            ('MX', 'Mexico', 'mexico', '2_LAT_AM'),
            ('MM', 'Myanmar', 'myanmar', '4_ASIA_SP'),
            ('NP', 'Nepal', 'nepal', '4_ASIA_SP'),
            ('NL', 'The Netherlands', 'the-netherlands', '3_EUR'),
            ('NI', 'Nicaragua', 'nicaragua', '2_LAT_AM'),
            ('NO', 'Norway', 'norway', '3_EUR'),
            ('PK', 'Pakistan', 'pakistan', '4_ASIA_SP'),
            ('PS', 'Palestine', 'palestine', '5_A_ME'),
            ('PY', 'Paraguay', 'paraguay', '2_LAT_AM'),
            ('PE', 'Peru', 'peru', '2_LAT_AM'),
            ('PH', 'Philippines', 'philippines', '4_ASIA_SP'),
            ('PL', 'Poland', 'poland', '3_EUR'),
            ('PT', 'Portugal', 'portugal', '3_EUR'),
            ('RO', 'Romania', 'romania', '3_EUR'),
            ('RU', 'Russia', 'russia', '3_EUR'),
            ('SN', 'Senegal', 'senegal', '5_A_ME'),
            ('RS', 'Serbia', 'serbia', '3_EUR'),
            ('SG', 'Singapore', 'singapore', '4_ASIA_SP'),
            ('SK', 'Slovakia', 'slovakia', '3_EUR'),
            ('SI', 'Slovenia', 'slovenia', '3_EUR'),
            ('KR', 'South Korea', 'south-korea', '4_ASIA_SP'),
            ('ES', 'Spain', 'spain', '3_EUR'),
            ('LK', 'Sri Lanka', 'sri-lanka', '4_ASIA_SP'),
            ('CH', 'Switzerland', 'switzerland', '3_EUR'),
            ('TW', 'Taiwan', 'taiwan', '4_ASIA_SP'),
            ('TH', 'Thailand', 'thailand', '4_ASIA_SP'),
            ('TN', 'Tunisia', 'tunisia', '5_A_ME'),
            ('TR', 'Turkey', 'turkey', '3_EUR'),
            ('UG', 'Uganda', 'uganda', '5_A_ME'),
            ('UA', 'Ukraine', 'ukraine', '3_EUR'),
            ('GB', 'United Kingdom', 'united-kingdom', '3_EUR'),
            ('US', 'United States', 'united-states', 'US_CAN'),
            ('UY', 'Uruguay', 'uruguay', '2_LAT_AM'),
            ('VE', 'Venezuela', 'venezuela', '2_LAT_AM'),
            ('VN', 'Vietnam', 'vietnam', '4_ASIA_SP'),
            ('ZW', 'Zimbabwe', 'zimbabwe', '5_A_ME'),
        )

    def forwards(self, orm):
        Community = orm.Community
        communities = self.get_communities()
        keys = ('code', 'name', 'slug', 'region')

        for community in communities:
            Community(**(dict(zip(keys, community)))).save()


    def backwards(self, orm):
        Community = orm.Community
        communities = self.get_communities()
        codes = map(lambda i: i[0], communities)

        Community.objects.find(pk__in=codes).delete()


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'people.community': {
            'Meta': {'object_name': 'Community'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'people.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Community']", 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['people']
    symmetrical = True
