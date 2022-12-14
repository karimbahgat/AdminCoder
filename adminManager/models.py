from django.db import models
from django.db.models.functions import Upper

from django.forms.models import model_to_dict

from djangowkb.fields import GeometryField

# Create your models here.

class Admin(models.Model):
    parent = models.ForeignKey('Admin', related_name='children', on_delete=models.CASCADE, 
                                blank=True, null=True)
    source = models.ForeignKey('AdminSource', related_name='admins', on_delete=models.CASCADE, 
                                blank=True, null=True)
    names = models.ManyToManyField('AdminName', related_name='admins')
    level = models.IntegerField(null=True, blank=True) # just to indicate the self-described admin-level of the ref
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    geom = GeometryField() #null=True, blank=True)

    minx = models.FloatField(null=True, blank=True)
    miny = models.FloatField(null=True, blank=True)
    maxx = models.FloatField(null=True, blank=True)
    maxy = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['minx','miny','maxx','maxy']), 
        ]

    def __str__(self):
        hierarchy_names = [p.names.first().name for p in self.get_all_parents()]
        return f'{", ".join(hierarchy_names)}'

    def save(self, *args, **kwargs):
        # auto set bbox attrs
        #if self.geom and self.geom.wkb: # TODO: need to fix django-wkb to handle empty wkb strings and/or use None instead
        #    self.minx,self.miny,self.maxx,self.maxy = self.geom.bbox()
        # normal save
        super(Admin, self).save(*args, **kwargs)

    @property
    def lineres(self):
        # not very efficient
        from core.utils import calc_stats
        geom = self.geom.__geo_interface__
        feat = {'type':'Feature', 'geometry':geom}
        stats = calc_stats(feats=[feat])
        return stats['statsLineResolution']

    def get_all_parents(self, include_self=True):
        '''Returns a list of all parents, starting with and including self.'''
        refs = [self]
        cur = self
        while cur.parent:
            cur = cur.parent
            refs.append(cur)
        return refs

    def get_all_children(self):
        '''Returns a list of all children.'''
        results = []
        for child in self.children.all():
            subchildren = child.get_all_children()
            results.append( {'item':child, 'children':subchildren} )
        return results

    def full_name(self):
        all_refs = self.get_all_parents()
        full_name = ', '.join([ref.names.first().name for ref in all_refs])
        return full_name

    def serialize(self, geom=True):
        hierarchy = [{'id':p.id, 
                        'names':[n.name for n in p.names.all()], 
                        'level':p.level,
                        }
                        for p in self.get_all_parents()]
        source = self.source
        dct = {'id':self.pk,
                'hierarchy':hierarchy,
                'source':{'name':source.name, 'id':source.pk},
                'valid_from':self.valid_from,
                'valid_to':self.valid_to,
                'lineres':self.lineres,
                }
        if geom:
            dct['geom'] = self.geom.__geo_interface__
        return dct

class AdminName(models.Model):
    name = models.CharField(max_length=100)

    # for now just manually add index w collate nocase
    #class Meta:
    #    indexes = [
    #        models.Index(Upper('name'),
    #                    name='adminManage_name_upper_idx'), 
    #    ]

    def __str__(self):
        return f'{self.name}'

class AdminSource(models.Model):
    SOURCE_TYPES = [
        ('DataSource', 'Data Source'),
        ('MapSource', 'Map Source'),
    ]
    type = models.CharField(max_length=50,
                            choices=SOURCE_TYPES)
    name = models.CharField(max_length=200)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    citation = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
