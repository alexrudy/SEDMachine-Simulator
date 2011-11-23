import numpy as np
import scipy as sp
import pylab as pl
import scipy.interpolate, scipy.integrate
from massey import skyab


def abmag_to_flambda(AB # Ab magnitude
	, lam): # Wavelength in angstrom

	c = 2.9979e18 # angstrom/s

	# return erg/s/cm^2/ang
	return 10**(-(AB + 48.6)/2.5)*c/lam**2

def vegamag_to_flambda(m, band):
	if band == 'r':
		pass


skyflam = np.transpose(np.array([skyab[:,0], abmag_to_flambda(skyab[:,1], skyab[:,0])]))
pl.ion()

hc = 1.98644521e-8 # erg angstrom


# See derivation on pg 83 of SED NB 1 (20 July 2011)
moon_phase = np.array([0., 0.08, 0.16, 0.24, 0.32, 0.40, 0.50])
moon_g = np.array([2e-17, 2.1e-17, 2.15e-17, 2.3e-17, 5.3e-17, 1.7e-16, 3.2e-16])
moon_r = np.array([2.3e-17,2.3e-17,2.3e-17,3.3e-17,3.5e-17,8.3e-17,1.3e-16])
moon_i = np.array([2.8e-17,3.0e-17,3.0e-17,3.3e-17,3.8e-17,7.0e-17,9.0e-17])

sky_ls = (4868., 6290., 7706., 10000)


pl.figure(7)
pl.clf()
moon_funs = []
for i in xrange(len(moon_phase)):
	gm = moon_g[i]-moon_g[0]
	rm = moon_r[i]-moon_r[0]
	im = moon_i[i]-moon_i[0]
	zm = im

	ff= np.poly1d(np.polyfit(sky_ls, np.array([gm, rm, im, zm]), 2))

	pl.plot(sky_ls, [gm, rm, im, zm], 'o')
	ll = np.arange(3700, 10000)
	pl.plot(ll, ff(ll))

	moon_funs.append(ff)


# From Hanuschik
uves_sky = np.array([
	(5730	, -0.2857),
	(6546	, -0.2857),
	(6815	, -0.9870),
	(6860	, -1.064),
	(6893	, -1.084),
	(6960	, -1.084),
	(7005	, -1.084),
	(7061	, -0.9090),
	(7095	, -0.9090),
	(7151	, -0.8311),
	(7195	, -0.9870),
	(7262	, -1.006),
	(7330	, -1.064),
	(7386	, -1.064),
	(7497	, -0.7532),
	(7598	, -0.6363),
	(7632	, -0.7532),
	(7699	, -0.8311),
	(7755	, -0.8896),
	(7811	, -0.8506),
	(7855	, -0.8701),
	(7911	, -0.9870),
	(7967	, -0.9675),
	(8001	, -0.9090),
	(8012	, -0.6363),
	(8079	, -0.4999),
	(8169	, -0.4805),
	(8225	, -0.5389),
	(8292	, -0.5389),
	(8325	, -0.7337),
	(8393	, -0.8506),
	(8437	, -1.006),
	(8482	, -1.084),
	(8549	, -1.123),
	(8583	, -0.5194),
	(8650	, -0.4999),
	(8695	, -0.3051),
	(8751	, -0.3831),
	(8806	, -0.5779),
	(8851	, -0.7532),
	(8918	, -0.9675),
	(8952	, -0.4999),
	(9019	, -0.4025),
	(9075	, -1.006),
	(9097	, -0.4025),
	(9109	, -0.2272),
	(9165	, -0.2662),
	(9232	, -0.4025),
	(9276	, -0.3246),
	(9332	, -0.4805),
	(9400	, -0.5974),
	(9444	, -1.045),
	(9489	, -1.103),
	(9545	, -1.084),
	(9601	, -1.084),
	(9657	, -1.103),
	(9702	, -0.07142),
	(9746	, -0.1883),
	(9813	, -0.2662),
	(9869	, -0.2857),
	(9925	, -0.3441),
	(9970	, -0.4999),
	(10030	, -0.6948),
	(10070	, -0.4025),
	(10120	, -0.4025),
	(10180	, -0.1883),
	(10230	, -0.5779),
	(10290	, -0.2662),
	(10320	, 0.02597),
	(10390	, -0.1493),
	(10440	, 0.006493),
	(10490	, -0.1688),
	(10550	, -0.1688),
	(10600	, 0.1038),
	(10660	, -0.01298),
	(10700	, 0.2402),
	(10750	, -0.2272)
])

uves_sky[:,1] = 10**(uves_sky[:,1])*1e-17 # erg/sec/cm^2/Ang/Arc^2
uves_sky[:,1] /= (hc/uves_sky[:,0]) # #/sec/cm^2/Ang/Arc^2

# From Turnrose PASP 86 (1974)
# Wavelength [A],  10^-18 erg / sec / cm^2 / Angstrom / Arcsecond^2
skyspec = [
	(3180, 4.30),
	(3260, 5.18),
	(3340, 6.13),
	(3420, 4.75),
	(3500, 4.86),
	(3580, 5.29),
	(3660, 7.24),
	(3740, 4.75),
	(3820, 4.43),
	(3900, 3.45),
	(3980, 4.31),
	(4060, 8.58),
	(4140, 6.09),
	(4220, 5.83),
	(4300, 5.39),
	(4380, 11.40),
	(4460, 6.25),
	(4540, 6.38),
	(4620, 6.16),
	(4700, 6.27),
	(4780, 6.14),
	(4860, 6.45),
	(4940, 6.24),
	(5020, 5.60),
	(5100, 5.80),
	(5180, 6.37),
	(5260, 6.26),
	(5340, 6.56),
	(5420, 7.85),
	(5500, 11.00),
	(5580, 25.40),
	(5660, 7.78),
	(5740, 9.70),
	(5760, 9.43),
	(5920, 11.40),
	(6080, 7.89),
	(6240, 13.00),
	(6400, 9.60),
	(6560, 8.36),
	(6720, 6.67),
	(6880, 9.73),
	(7040, 7.11),
	(7200, 9.53),
	(7360, 13.80),
	(7520, 10.70),
	(7680, 13.20),
	(7840, 23.60),
	(8000, 16.60),
	(8160, 5.54),
	(8320, 22.70),
	(8480, 19.30),
	(8640, 20.10),
	(8800, 36.10),
	(8960, 28.30),
	(9120, 8.22),
	(9280, 21.40),
	(9440, 32.40),
	(9600, 15.80),
	(9760, 26.30),
	(9920, 66.00),
	(10080, 68.30),
	(10240, 99.60),
	(10400, 87.10),
	(10560, 25.80),
	(10720, 64.30),
	(10880, 134.00)
]


pl.ion()

PHASEIX = 0
skyspec = np.array(skyspec)
skyspec[:,1] *= 1e-18 * 3 
skyspec[:,1] += moon_funs[PHASEIX](skyspec[:,0])
skyspec[:,1] /= hc/skyspec[:,0] # #/s/cm^2/ang/as^2


quimby_sky = [
       (3700.0000  , 2.02717e-17),
       (3715.4167  , 2.06665e-17),
       (3730.8334  , 1.98731e-17),
       (3746.2501  , 1.79182e-17),
       (3761.6668  , 1.62443e-17),
       (3777.0835  , 1.54234e-17),
       (3792.5002  , 1.50922e-17),
       (3807.9169  , 1.49957e-17),
       (3823.3336  , 1.50155e-17),
       (3838.7503  , 1.46242e-17),
       (3854.1670  , 1.38789e-17),
       (3869.5837  , 1.34479e-17),
       (3885.0004  , 1.43856e-17),
       (3900.4171  , 1.68993e-17),
       (3915.8338  , 1.80565e-17),
       (3931.2505  , 1.65088e-17),
       (3946.6672  , 1.54510e-17),
       (3962.0839  , 1.52556e-17),
       (3977.5006  , 1.57588e-17),
       (3992.9173  , 1.78360e-17),
       (4008.3340  , 2.16229e-17),
       (4023.7507  , 2.88447e-17),
       (4039.1674  , 3.73874e-17),
       (4054.5841  , 3.86219e-17),
       (4070.0008  , 3.17286e-17),
       (4085.4175  , 2.50495e-17),
       (4100.8342  , 2.09098e-17),
       (4116.2509  , 1.87478e-17),
       (4131.6676  , 1.88843e-17),
       (4147.0843  , 1.99333e-17),
       (4162.5010  , 2.03872e-17),
       (4177.9177  , 1.95844e-17),
       (4193.3344  , 1.83386e-17),
       (4208.7511  , 1.79008e-17),
       (4224.1678  , 1.82422e-17),
       (4239.5845  , 1.88881e-17),
       (4255.0012  , 1.87869e-17),
       (4270.4179  , 1.80552e-17),
       (4285.8346  , 1.79907e-17),
       (4301.2513  , 1.92960e-17),
       (4316.6680  , 2.31423e-17),
       (4332.0847  , 3.33152e-17),
       (4347.5014  , 5.05596e-17),
       (4362.9181  , 5.68220e-17),
       (4378.3348  , 4.38804e-17),
       (4393.7515  , 2.88135e-17),
       (4409.1682  , 2.26326e-17),
       (4424.5849  , 2.07390e-17),
       (4440.0016  , 1.97088e-17),
       (4455.4183  , 1.89613e-17),
       (4470.8350  , 1.89928e-17),
       (4486.2517  , 1.94766e-17),
       (4501.6684  , 1.97767e-17),
       (4517.0851  , 1.96447e-17),
       (4532.5018  , 1.91473e-17),
       (4547.9185  , 1.87819e-17),
       (4563.3352  , 1.84063e-17),
       (4578.7519  , 1.79644e-17),
       (4594.1686  , 1.76399e-17),
       (4609.5853  , 1.74064e-17),
       (4625.0020  , 1.75218e-17),
       (4640.4187  , 1.82677e-17),
       (4655.8354  , 1.98184e-17),
       (4671.2521  , 2.08446e-17),
       (4686.6688  , 2.04041e-17),
       (4702.0855  , 2.01972e-17),
       (4717.5022  , 2.11294e-17),
       (4732.9189  , 2.22260e-17),
       (4748.3356  , 2.16006e-17),
       (4763.7523  , 1.92745e-17),
       (4779.1690  , 1.73694e-17),
       (4794.5857  , 1.67303e-17),
       (4810.0024  , 1.73684e-17),
       (4825.4191  , 1.85540e-17),
       (4840.8358  , 1.95587e-17),
       (4856.2525  , 1.98990e-17),
       (4871.6692  , 1.97243e-17),
       (4887.0859  , 1.95257e-17),
       (4902.5026  , 1.92954e-17),
       (4917.9193  , 1.88088e-17),
       (4933.3360  , 1.88256e-17),
       (4948.7527  , 2.02459e-17),
       (4964.1694  , 2.32068e-17),
       (4979.5861  , 2.53933e-17),
       (4995.0028  , 2.44094e-17),
       (5010.4195  , 2.09629e-17),
       (5025.8362  , 1.79445e-17),
       (5041.2529  , 1.69708e-17),
       (5056.6696  , 1.83172e-17),
       (5072.0863  , 2.07792e-17),
       (5087.5030  , 2.17818e-17),
       (5102.9197  , 2.03520e-17),
       (5118.3364  , 1.79890e-17),
       (5133.7531  , 1.64045e-17),
       (5149.1698  , 1.57399e-17),
       (5164.5865  , 1.52761e-17),
       (5180.0032  , 1.49107e-17),
       (5195.4199  , 1.47379e-17),
       (5210.8366  , 1.48299e-17),
       (5226.2533  , 1.46491e-17),
       (5241.6700  , 1.44279e-17),
       (5257.0867  , 1.41880e-17),
       (5272.5034  , 1.39978e-17),
       (5287.9201  , 1.41026e-17),
       (5303.3368  , 1.41006e-17),
       (5318.7535  , 1.42491e-17),
       (5334.1702  , 1.45815e-17),
       (5349.5869  , 1.45390e-17),
       (5365.0036  , 1.75018e-17),
       (5380.4203  , 1.79547e-17),
       (5395.8370  , 1.95909e-17),
       (5411.2537  , 2.30146e-17),
       (5426.6704  , 2.85516e-17),
       (5442.0871  , 3.52529e-17),
       (5457.5038  , 3.97834e-17),
       (5472.9205  , 3.82465e-17),
       (5488.3372  , 3.15343e-17),
       (5503.7539  , 2.50815e-17),
       (5519.1706  , 2.18317e-17),
       (5534.5873  , 2.25199e-17),
       (5550.0040  , 2.75789e-17),
       (5565.4207  , 3.38273e-17),
       (5580.8374  , 3.58359e-17),
       (5596.2541  , 3.14500e-17),
       (5611.6708  , 2.47813e-17),
       (5627.0875  , 2.10099e-17),
       (5642.5042  , 2.19801e-17),
       (5657.9209  , 2.69619e-17),
       (5673.3376  , 3.28435e-17),
       (5688.7543  , 3.59927e-17),
       (5704.1710  , 2.93502e-17),
       (5719.5877  , 2.59874e-17),
       (5735.0044  , 2.39082e-17),
       (5750.4211  , 2.47406e-17),
       (5765.8378  , 2.74159e-17),
       (5781.2545  , 2.96842e-17),
       (5796.6712  , 3.05582e-17),
       (5812.0879  , 3.13459e-17),
       (5827.5047  , 3.42779e-17),
       (5842.9214  , 4.23417e-17),
       (5858.3381  , 5.68780e-17),
       (5873.7548  , 7.42556e-17),
       (5889.1715  , 8.42980e-17),
       (5904.5882  , 7.98210e-17),
       (5920.0049  , 6.54833e-17),
       (5935.4216  , 5.15890e-17),
       (5950.8383  , 4.27081e-17),
       (5966.2550  , 3.76377e-17),
       (5981.6717  , 3.42286e-17),
       (5997.0884  , 3.12527e-17),
       (6012.5051  , 2.87365e-17),
       (6027.9218  , 2.66659e-17),
       (6043.3385  , 2.50699e-17),
       (6058.7552  , 2.43229e-17),
       (6074.1719  , 2.48398e-17),
       (6089.5886  , 2.61423e-17),
       (6105.0053  , 2.77072e-17),
       (6120.4220  , 2.82387e-17),
       (6135.8387  , 2.75091e-17),
       (6151.2554  , 2.58070e-17),
       (6166.6721  , 2.38614e-17),
       (6182.0888  , 2.19971e-17),
       (6197.5055  , 2.09375e-17),
       (6212.9222  , 2.09052e-17),
       (6228.3389  , 2.13585e-17),
       (6243.7556  , 2.21405e-17),
       (6259.1723  , 2.36819e-17),
       (6274.5890  , 2.58043e-17),
       (6290.0057  , 2.74759e-17),
       (6305.4224  , 2.70779e-17),
       (6320.8391  , 2.48590e-17),
       (6336.2558  , 2.22284e-17),
       (6351.6725  , 2.01509e-17),
       (6367.0892  , 1.87647e-17),
       (6382.5059  , 1.73881e-17),
       (6397.9226  , 1.59926e-17),
       (6413.3393  , 1.48660e-17),
       (6428.7560  , 1.42760e-17),
       (6444.1727  , 1.41329e-17),
       (6459.5894  , 1.43061e-17),
       (6475.0061  , 1.45802e-17),
       (6490.4228  , 1.48264e-17),
       (6505.8395  , 1.50530e-17),
       (6521.2562  , 1.50986e-17),
       (6536.6729  , 1.50332e-17),
       (6552.0896  , 1.47718e-17),
       (6567.5063  , 1.41401e-17),
       (6582.9230  , 1.34251e-17),
       (6598.3397  , 1.26021e-17),
       (6613.7564  , 1.18839e-17),
       (6629.1731  , 1.13306e-17),
       (6644.5898  , 1.10631e-17),
       (6660.0065  , 1.10109e-17),
       (6675.4232  , 1.10653e-17),
       (6690.8399  , 1.11530e-17),
       (6706.2566  , 1.12871e-17),
       (6721.6733  , 1.11769e-17),
       (6737.0900  , 1.08230e-17),
       (6752.5067  , 1.05216e-17),
       (6767.9234  , 1.05025e-17),
       (6783.3401  , 1.08966e-17),
       (6798.7568  , 1.19171e-17),
       (6814.1735  , 1.33633e-17),
       (6829.5902  , 1.46448e-17),
       (6845.0069  , 1.53078e-17),
       (6860.4236  , 1.53730e-17),
       (6875.8403  , 1.50981e-17),
       (6891.2570  , 1.46979e-17),
       (6906.6737  , 1.45079e-17),
       (6922.0904  , 1.44862e-17),
       (6937.5071  , 1.42225e-17),
       (6952.9238  , 1.35759e-17),
       (6968.3405  , 1.27919e-17),
       (6983.7572  , 1.20665e-17),
       (6999.1739  , 1.15150e-17),
       (7014.5906  , 1.11709e-17),
       (7030.0073  , 1.09678e-17),
       (7045.4240  , 1.07658e-17),
       (7060.8407  , 1.05352e-17),
       (7076.2574  , 1.02745e-17),
       (7091.6741  , 1.00581e-17),
       (7107.0908  , 9.88300e-18),
       (7122.5075  , 9.80131e-18),
       (7137.9242  , 9.67843e-18),
       (7153.3409  , 9.64314e-18),
       (7168.7576  , 9.76343e-18),
       (7184.1743  , 1.04100e-17),
       (7199.5910  , 1.20370e-17),
       (7215.0077  , 1.46201e-17),
       (7230.4244  , 1.76306e-17),
       (7245.8411  , 2.02239e-17),
       (7261.2578  , 2.18849e-17),
       (7276.6745  , 2.26972e-17),
       (7292.0912  , 2.30904e-17),
       (7307.5079  , 2.33583e-17),
       (7322.9246  , 2.35029e-17),
       (7338.3413  , 2.32091e-17),
       (7353.7580  , 2.21542e-17),
       (7369.1747  , 2.05812e-17),
       (7384.5914  , 1.87210e-17),
       (7400.0081  , 1.69094e-17),
       (7415.4248  , 1.55367e-17),
       (7430.8415  , 1.47677e-17),
       (7446.2582  , 1.46516e-17),
       (7461.6749  , 1.48456e-17),
       (7477.0916  , 1.53064e-17),
       (7492.5083  , 1.57086e-17),
       (7507.9250  , 1.58806e-17),
       (7523.3417  , 1.59003e-17),
       (7538.7584  , 1.55611e-17),
       (7554.1751  , 1.47929e-17),
       (7569.5918  , 1.37116e-17),
       (7585.0085  , 1.24384e-17),
       (7600.4252  , 1.13264e-17),
       (7615.8419  , 1.06194e-17),
       (7631.2586  , 1.05623e-17),
       (7646.6753  , 1.14172e-17),
       (7662.0920  , 1.34761e-17),
       (7677.5087  , 1.67288e-17),
       (7692.9254  , 2.06568e-17),
       (7708.3421  , 2.43563e-17),
       (7723.7588  , 2.71983e-17),
       (7739.1755  , 2.86795e-17),
       (7754.5922  , 2.90773e-17),
       (7770.0089  , 2.91224e-17),
       (7785.4256  , 2.93998e-17),
       (7800.8423  , 3.01568e-17),
       (7816.2590  , 3.12877e-17),
       (7831.6757  , 3.27212e-17),
       (7847.0924  , 3.39644e-17),
       (7862.5091  , 3.47962e-17),
       (7877.9258  , 3.50905e-17),
       (7893.3425  , 3.50047e-17),
       (7908.7592  , 3.44340e-17),
       (7924.1759  , 3.34871e-17),
       (7939.5926  , 3.25377e-17),
       (7955.0093  , 3.16620e-17),
       (7970.4260  , 3.08675e-17),
       (7985.8427  , 2.98951e-17),
       (8001.2594  , 2.81604e-17),
       (8016.6761  , 2.58169e-17),
       (8032.0928  , 2.30331e-17),
       (8047.5095  , 2.03176e-17),
       (8062.9262  , 1.78698e-17),
       (8078.3429  , 1.59822e-17),
       (8093.7596  , 1.46681e-17),
       (8109.1763  , 1.39332e-17),
       (8124.5930  , 1.39190e-17),
       (8140.0097  , 1.48306e-17),
       (8155.4264  , 1.65150e-17),
       (8170.8431  , 1.83917e-17),
       (8186.2598  , 1.96968e-17),
       (8201.6765  , 2.00720e-17),
       (8217.0932  , 1.99681e-17),
       (8232.5099  , 2.03962e-17),
       (8247.9266  , 2.23062e-17),
       (8263.3433  , 2.57101e-17),
       (8278.7600  , 2.98004e-17),
       (8294.1767  , 3.36014e-17),
       (8309.5934  , 3.65482e-17),
       (8325.0101  , 3.87147e-17),
       (8340.4268  , 4.00345e-17),
       (8355.8435  , 4.08204e-17),
       (8371.2602  , 4.11680e-17),
       (8386.6769  , 4.13338e-17),
       (8402.0936  , 4.13780e-17),
       (8417.5103  , 4.08000e-17),
       (8432.9270  , 3.93746e-17),
       (8448.3437  , 3.66761e-17),
       (8463.7604  , 3.32712e-17),
       (8479.1771  , 2.95171e-17),
       (8494.5938  , 2.57516e-17)
]

quimby_sky = np.array(quimby_sky)

skyf = sp.interpolate.interp1d(skyspec[:,0], skyspec[:,1])


pl.figure(1)
pl.clf()
l = skyspec[:,0]
s = skyspec[:,1]
pl.semilogy(l,s*hc/l,'o-')
#pl.semilogy(skyflam[:,0], skyflam[:,1])
pl.semilogy(quimby_sky[:,0], quimby_sky[:,1])



GAIN = 2.

pix_per_res = 2.4
window_width = 6.0
num_spec = 7.0
npix = pix_per_res * window_width * num_spec

cameras = {
	"PI": {"DQEs": np.array([
		(2000, 0),	
		(3000, 0.01),
		(3500, .20),
		(4000, .60),
		(4500, .82),
		(5000, .90),
		(5500, .93),
		(6000, .93),
		(7000, .93),
		(7500, .88),
		(8000, .73),
		(8500, .55),
		(9000, .33),
		(10000, .08),
		(10500, 0.02),
		(11000, 0)
	]),
	"RN" : 4.,
	"DC":  0.006,
	"readtime": 37*3},
	"Andor": { # Midband
		"DQEs": np.array([
		(2500, .05),
		(3500, .18),
		(4500, .75),
		(5000, .9),
		(5500, .92),
		(6500, .91),
		(7500, .79),
		(8500, .48),
		(9500, .13),
		(10500, .02),
		(11000, 0)
	]), 
	"RN": 2.9,
	"DC": 0.0004,
	"readtime":  82*3},
	"E2V": {"DQEs" : np.array([
		(3000, .1),
		(3500, .3),
		(4500, .8),
		(5500, .8),
		(6500, .78),
		(7500, .7),
		(8500, .4),
		(9500, .13),
		(10500, .02),
		(11000, 0)]),
	"RN": 5,
	"DC": 0.006,
	"readtime": 37*3}}


import atmosphere
ext = atmosphere.ext

p60area = 18242. * 0.9 # cm^2
airmass = 1.2

# Source spectrum in units of 
# #/s/Angstrom/cm^2
def source(lam):
	ff = np.poly1d(np.polyfit([3000, 10000], [3.66e-6, 3.66e-6], 0))

	return ff(lam)

pl.figure(1)
l = np.arange(3300, 10500,200)
pl.plot(l, source(l)*hc/l)
pl.xlabel(u"$\lambda$ [$\AA$]")
pl.ylabel(u"flux [$erg$ $s^{-1}$ $cm^{-2}$ $\AA^{-1}$ $arcsec^{-2}$]")
pl.xlim([3700,10000])
pl.legend(["Sky", "Massey sky", "21 mag source"], loc="upper right")
pl.title(u"Source and Sky Spectrum $\phi$: %0.2f" % (moon_phase[PHASEIX]))
pl.show()
pl.savefig("source_v_sky_%0.2f.pdf" % (moon_phase[PHASEIX]))

thpts = np.load("thpt.npy")[0]
qeprism = sp.interpolate.interp1d(thpts["lambda"], thpts["thpt-prism-PI"])
qegrating = sp.interpolate.interp1d(thpts["lambda"], thpts["thpt-grating"])

def instrument_efficiency(l, qe):
	return 10**(-ext(l)*airmass/2.5) * qegrating(l)

def num_photons(fun, exptime, area, lam1, lam2):
	num_photon = sp.integrate.quad(fun, lam1, lam2, limit=150)[0] * exptime * area 

	return num_photon

R = 100. # Spectral Resolution
aperture_area = 3.0 * 3.0

def calculate(ET, camera_name):
	startl = 3700.
	endl = startl + startl/R
	ls = []
	nsky_photon = []
	nsource_photon = []

	camera = cameras[camera_name]
	DQEs = camera["DQEs"]
	qe = sp.interpolate.interp1d(DQEs[:, 0], DQEs[:, 1], kind='cubic')
	RN = camera["RN"]
	DC = camera["DC"]
	exptime = ET - camera["readtime"]
	print "Integrating. RN %f" % RN
	while startl < 9500:
		l = (startl+endl)/2
		nsky_photon.append(num_photons(skyf, exptime, p60area, startl, endl) * 
			instrument_efficiency(l, qe) * aperture_area)
		nsource_photon.append(num_photons(source, exptime, p60area, startl, endl) * 
			instrument_efficiency(l, qe))
		ls.append(l)

		startl = endl
		endl = startl + startl/R

	(ls, nsky_photon, nsource_photon) = map(np.array, (ls, nsky_photon, nsource_photon))
	shot_noise = np.sqrt(nsky_photon + nsource_photon + npix/GAIN * RN**2 + npix * DC * exptime)

	loi = 4000
	print "At %i nm:" % (loi/10)
	print "Efficiency: %1.2f" % (instrument_efficiency(loi, qe))
	
	print "Area: %6.0f cm^2 Exptime: %6.0f s" % (p60area, exptime)
	print

	i6000 = np.argmin(np.abs(ls-loi))
	sky6000 = num_photons(skyf, exptime, p60area, loi-loi/R/2., loi+loi/R/2.) * \
		instrument_efficiency(loi, qe) * aperture_area
	source6000 = num_photons(source, exptime, p60area, loi-loi/R/2., loi+loi/R/2.) * \
		instrument_efficiency(loi, qe)

	print "source photons: %6.1f       sky: %6.1f per R" % (source6000, sky6000)
	print "  source noise: %6.1f sky noise: %6.1f  RN: %6.1f DCN: %6.1f per R" % (
		np.sqrt(source6000), np.sqrt(sky6000), 
		np.sqrt(npix/GAIN*RN**2), np.sqrt(npix*DC*exptime))

	print "================"
	noise = np.sqrt(sky6000 + source6000 + npix*RN**2 + DC * npix * exptime)
	print "   total noise: %6.1f  ---> S/N: %6.1f per R" % (noise, source6000/noise)

	print
	

	print "Again %i nm" % (loi/10)
	dlambda = (ls[i6000+1] - ls[i6000])
	print "Source #/s/A/cm^2: %6.1e sky: %6.1e" % (
		source(loi), skyf(loi))
	print "Source #/s/A/cm^2: %6.1e sky: %6.1e (modulo efficiency)" % (
		source6000 / exptime / p60area / dlambda,
		sky6000 / exptime / p60area / dlambda * aperture_area)
		
	
	pl.figure(3)
	pl.clf()
	pl.title(u"Detected Counts [%s | $\phi$: %0.2f]" % (camera_name, moon_phase[PHASEIX]))
	pl.semilogy(ls, nsource_photon, linewidth=2)
	pl.semilogy(ls, np.sqrt(nsky_photon + nsource_photon + npix*RN**2 
		+ npix*DC*exptime),linewidth=3)
	pl.semilogy(ls, nsky_photon)
	pl.semilogy(ls, np.ones(len(ls))*npix*RN)
	pl.semilogy(ls, np.ones(len(ls))*npix*DC*exptime)
	pl.axvline(3700)
	pl.ylim([10,1e5])
	pl.xlabel(u"$\lambda$ [$\AA$]")
	pl.ylabel("Counts per Resolution Element (1200 s exp)")

	pl.legend(["21 mag Source", "Noise", u"Sky [D=%2.1f $as^2$]" % (aperture_area), "RN=%i/pix (G=%1.1f, N=%i)" % (RN, GAIN, npix), "DC=%1.3f/pix/s" % (DC)], loc='upper left')

	ax2 = pl.twinx()
	l = np.arange(3700, 9500)
	ax2.plot(l,instrument_efficiency(l, qe), '--')
	pl.ylim([0,1])
	pl.ylabel("Instrument QE")

	pl.xlim([3500,10000])
	pl.savefig("counts_%s_%0.2f.pdf" % (camera_name, moon_phase[PHASEIX]))


	fig = pl.figure(4)
	pl.clf()
	pl.axvline(3700)
	ax1 = fig.add_subplot(111)
	pl.title(u"S/N for 21 mag source [%s | Moon$\phi$: %0.2f]" % (camera_name, moon_phase[PHASEIX]))
	pl.plot(ls, nsource_photon/shot_noise)
	#pl.semilogy(ls, nsource_photon/shot_noise)
	pl.ylim([0, 20])
	pl.xlim([3500,10000])
	pl.xlabel(u"$\lambda$ ($\AA$)")
	pl.ylabel(u"$S/N$ per $R$")
	pl.axhline([10],color='r')
	pl.axhline([10/np.sqrt(3)],color='r')
	pl.grid('on', which='minor')
	pl.savefig("sn_%s_%0.2f.pdf" % (camera_name, moon_phase[PHASEIX]))

	np.save("sn_%s_%0.2f" % (camera_name, moon_phase[PHASEIX]), [{"lambda": ls, "source": nsource_photon, "noise": shot_noise}])

exptime = 1200
calculate(exptime, "PI")



