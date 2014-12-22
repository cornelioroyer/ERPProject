from django.conf import settings
ugettext = lambda s: s

Jenis_Material = getattr(settings, 'Jenis_Material',((1, ugettext('Major')),
														(2, ugettext('Minor')),
														(3, ugettext('Colour Material')),
														(4, ugettext('Uncolour')),
														(5, ugettext('Stabilitator')),
														(6, ugettext('Cat Label')),
														(7, ugettext('Case'))))
														
Warna_Produk = getattr(settings, 'Warna_Produk',((1, ugettext('Flint')),
													(2, ugettext('Amber')),
													(3, ugettext('Green'))))
													
Label_Produk = getattr(settings, 'Label_Produk',((1, ugettext('Polos')),
													(2, ugettext('Dekorasi'))))
													
					
Dapur = getattr(settings, 'Dapur',(('G.1.1 D.G', ugettext('G.1.1 D.G')),
									('G.1.2 D.G', ugettext('G.1.2 D.G')),
									('G.1.3 D.G', ugettext('G.1.3 D.G')),
									('G.2.1 D.G', ugettext('G.2.1 D.G')),
									('G.2.2 D.G', ugettext('G.2.2 D.G')),
									('G.2.3 D.G', ugettext('G.2.3 D.G'))))
									
Status_Dapur = getattr(settings, 'Status_Dapur',((1, ugettext('PRODUKSI')),
												(2, ugettext('STOP PRODUKSI'))))
									
ACL = getattr(settings, 'ACL',(('ACL-1', ugettext('ACL-1')),
									('ACL-2', ugettext('ACL-2')),
									('ACL-3', ugettext('ACL-3')),
									('ACL-4', ugettext('ACL-4'))))
									
Status_ACL = getattr(settings, 'Status_ACL',((1, ugettext('PRODUKSI')),
												(2, ugettext('STOP PRODUKSI'))))
												
TIM = getattr(settings, 'TIM',(('PRODUKSI', ugettext('PRODUKSI')),
											('ACL', ugettext('ACL')),
											('PENGEMASAN', ugettext('PENGEMASAN'))))
											
												
Initial = getattr(settings, 'Initial',(('A', ugettext('A')),
										('B', ugettext('B')),
										('C', ugettext('C')),
										('D', ugettext('D')),
										('E', ugettext('E')),
										('F', ugettext('F'))))
										
Inspect = getattr(settings, 'Inspect',((1, ugettext('Target')),
												(2, ugettext('Pencapaian'))))
												
LEVEL_AKSES_CHOICES =  getattr(settings, 'LEVEL_AKSES_CHOICES', (('Seksi', ugettext('Seksi')),
																	('Kadep', ugettext('Kadep')),
																	('Direktur', ugettext('Direktur')))) #nanti Direktur rubah ke kasi
																	
STACHOLDER =  getattr(settings, 'STACHOLDER', (('Departemen Inventori', ugettext('Departemen Inventori')),
																	('Departemen Sales', ugettext('Departemen Sales')),
																	('Departemen Assest', ugettext('Departemen Assest'))))
								

Kategori_Produk = getattr(settings, 'Kategori_Produk', ((1, ugettext('Generic')),
										(2, ugettext('Patent'))))				
												
									
