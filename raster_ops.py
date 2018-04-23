import gdal
import numpy as np

# Archivos de entrada
alt_file = "alt.tif"
prec_file = "precp.tif"
for_file = "BQNBQ_2016_EPSG4326.tif"

holdrigde_count = {}


def holdridge(altitude, precipitation):
	out = None
	if altitude < 1000:
		if 500 <= precipitation < 1000:
			out = 'tropical_very_dry'
		elif 1000 <= precipitation < 2000:
			out = 'tropical_dry'
		elif 2000 <= precipitation < 4000:
			out = 'tropical_moist'
		elif 4000 <= precipitation < 8000:
			out = 'tropical_wet'
		elif 8000 <= precipitation:
			out = 'tropical_rain'
		else:
			pass
	elif 1000 <= altitude < 2000:
		if 500 <= precipitation < 1000:
			out = 'premontane_dry'
		elif 1000 <= precipitation < 2000:
			out = 'premontane_moist'
		elif 2000 <= precipitation < 4000:
			out = 'premontane_wet'
		elif 4000 <= precipitation < 8000:
			out = 'premontane_rain'
		else:
			pass
	elif 2000 <= altitude < 3000:
		if 500 <= precipitation < 1000:
			out = 'lower_montane_dry'
		elif 1000 <= precipitation < 2000:
			out = 'lower_montane_moist'
		elif 2000 <= precipitation < 4000:
			out = 'lower_montane_wet'
		elif 4000 <= precipitation < 8000:
			out = 'lower_montane_rain'
		else:
			pass
	elif 3000 <= altitude < 4000:
		if 500 <= precipitation < 1000:
			out = 'montane_moist'
		elif 1000 <= precipitation < 2000:
			out = 'montane_wet'
		elif 2000 <= precipitation < 4000:
			out = 'montane_wet'
		else:
			pass
	else:
		pass

	return out





alt_ras = gdal.Open(alt_file)
prec_ras = gdal.Open(prec_file)
for_ras = gdal.Open(for_file)

transform = alt_ras.GetGeoTransform()
altXOrigin = transform[0]
altYOrigin = transform[3]
altPixelWidth = transform[1]
altPixelHeight = transform[5]

transform = for_ras.GetGeoTransform()
forXOrigin = transform[0]
forYOrigin = transform[3]
forPixelWidth = transform[1]
forPixelHeight = transform[5]

for_band = for_ras.GetRasterBand(1)

alt_band = alt_ras.GetRasterBand(1)
alt_arr = alt_band.ReadAsArray(0,0,alt_ras.RasterXSize, alt_ras.RasterYSize)

prec_band = prec_ras.GetRasterBand(1)
prec_arr = prec_band.ReadAsArray(0,0,prec_ras.RasterXSize, prec_ras.RasterYSize)


it = np.nditer((alt_arr, prec_arr), flags=['multi_index'])
while not it.finished:
	if it[0] >= 0 and it[1] > 0:
		holdr = holdridge(it[0], it[1])

		if holdr:
			row = it.multi_index[0]
			col = it.multi_index[1]
			lon = col * altPixelWidth + altXOrigin
			lat = row * altPixelHeight + altYOrigin

			if lon >= forXOrigin and lat <= forYOrigin:
				fpx = int((lon - forXOrigin) / forPixelWidth)
				fpy = int((lat - forYOrigin) / forPixelHeight)

				if fpx <= for_ras.RasterXSize and fpy <= for_ras.RasterYSize:
					for_val = for_band.ReadAsArray(fpx, fpy, 1, 1)

					if for_val and for_val[0][0] == 1:

						if not holdr in holdrigde_count:
							holdrigde_count[holdr] = 1
						else:
							holdrigde_count[holdr] += 1

	it.iternext()
	
print holdrigde_count
