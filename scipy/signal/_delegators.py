"""Delegators for alternative backends in scipy.signal.

The signature of `func_signature` must match the signature of signal.func.
The job of a `func_signature` is to know which arguments of `signal.func`
are arrays.

* signatures are generated by

--------------
 import inspect
 from scipy import signal

 names = [x for x in dir(signal) if not x.startswith('_')]
 objs = [getattr(signal, name) for name in names]
 funcs = [obj for obj in objs if inspect.isroutine(obj)]

 for func in funcs:
     try:
        sig = inspect.signature(func)
     except ValueError:
         sig = "( FIXME )"
     print(f"def {func.__name__}_signature{sig}:\n\treturn array_namespace(...
 )\n\n")
---------------

* which arguments to delegate on: manually trawled the documentation for
  array-like and array arguments

"""
import numpy as np
from scipy._lib._array_api import array_namespace
from scipy.ndimage._ni_support import _skip_if_int


def _skip_if_lti(arg):
    """Handle `system` arg overloads.

    ATM, only pass tuples through. Consider updating when cupyx.lti class
    is supported.
    """
    if isinstance(arg, tuple):
        return arg
    else:
        return (None,)


def _skip_if_str_or_tuple(window):
    """Handle `window` being a str or a tuple or an array-like.
    """
    if isinstance(window, str) or isinstance(window, tuple) or callable(window):
        return None
    else:
        return window


def _skip_if_poly1d(arg):
    return None if isinstance(arg, np.poly1d) else arg

###################

def abcd_normalize_signature(A=None, B=None, C=None, D=None):
    return array_namespace(A, B, C, D)


def argrelextrema_signature(data, *args, **kwds):
    return array_namespace(data)

argrelmax_signature = argrelextrema_signature
argrelmin_signature = argrelextrema_signature


def band_stop_obj_signature(wp, ind, passb, stopb, gpass, gstop, type):
    return array_namespace(passb, stopb)


def bessel_signature(N, Wn, *args, **kwds):
    return array_namespace(Wn)

butter_signature = bessel_signature


def cheby2_signature(N, rs, Wn, *args, **kwds):
    return array_namespace(Wn)


def cheby1_signature(N, rp, Wn, *args, **kwds):
    return array_namespace(Wn)


def ellip_signature(N, rp, rs, Wn, *args, **kwds):
    return array_namespace(Wn)


########################## XXX: no arrays in, arrays out
def besselap_signature(N, norm='phase'):
    return np

def buttap_signature(N):
    return np

def cheb1ap_signature(N, rp):
    return np


def cheb2ap_signature(N, rs):
    return np

def ellipap_signature(N, rp, rs):
    return np

def correlation_lags_signature(in1_len, in2_len, mode='full'):
    return np


def czt_points_signature(m, w=None, a=(1+0j)):
    return np


def gammatone_signature(freq, ftype, order=None, numtaps=None, fs=None):
    return np


def iircomb_signature(w0, Q, ftype='notch', fs=2.0, *, pass_zero=False):
    return np


def iirnotch_signature(w0, Q, fs=2.0):
    return np


def iirpeak_signature(w0, Q, fs=2.0):
    return np


def savgol_coeffs_signature(
    window_length, polyorder, deriv=0, delta=1.0, pos=None, use='conv'
):
    return np


def unit_impulse_signature(shape, idx=None, dtype=float):
    return np
############################


####################### XXX: no arrays, maybe arrays out
def buttord_signature(wp, ws, gpass, gstop, analog=False, fs=None):
    return np

def cheb1ord_signature(wp, ws, gpass, gstop, analog=False, fs=None):
    return np

def cheb2ord_signature(wp, ws, gpass, gstop, analog=False, fs=None):
    return np

def ellipord_signature(wp, ws, gpass, gstop, analog=False, fs=None):
    return np
###########################################


########### NB: scalars in, scalars out
def kaiser_atten_signature(numtaps, width):
    return np

def kaiser_beta_signature(a):
    return np

def kaiserord_signature(ripple, width):
    return np

def get_window_signature(window, Nx, fftbins=True):
    return np
#################################


def bode_signature(system, w=None, n=100):
    return array_namespace(*_skip_if_lti(system), w)

dbode_signature = bode_signature


def freqresp_signature(system, w=None, n=10000):
    return array_namespace(*_skip_if_lti(system), w)

dfreqresp_signature = freqresp_signature


def impulse_signature(system, X0=None, T=None, N=None):
    return array_namespace(*_skip_if_lti(system), X0, T)


def dimpulse_signature(system, x0=None, t=None, n=None):
    return array_namespace(*_skip_if_lti(system), x0, t)


def lsim_signature(system, U, T, X0=None, interp=True):
    return array_namespace(*_skip_if_lti(system), U, T, X0)


def dlsim_signature(system, u, t=None, x0=None):
    return array_namespace(*_skip_if_lti(system), u, t, x0)


def step_signature(system, X0=None, T=None, N=None):
    return array_namespace(*_skip_if_lti(system), X0, T)

def dstep_signature(system, x0=None, t=None, n=None):
    return array_namespace(*_skip_if_lti(system), x0, t)


def cont2discrete_signature(system, dt, method='zoh', alpha=None):
    return array_namespace(*_skip_if_lti(system))


def bilinear_signature(b, a, fs=1.0):
    return array_namespace(b, a)


def bilinear_zpk_signature(z, p, k, fs):
    return array_namespace(z, p)


def chirp_signature(t,*args, **kwds):
    return array_namespace(t)


############## XXX: array-likes in, str out
def choose_conv_method_signature(in1, in2, *args, **kwds):
    return array_namespace(in1, in2)
############################################


def convolve_signature(in1, in2, *args, **kwds):
    return array_namespace(in1, in2)

fftconvolve_signature = convolve_signature
oaconvolve_signature = convolve_signature
correlate_signature = convolve_signature
correlate_signature = convolve_signature
convolve2d_signature = convolve_signature
correlate2d_signature = convolve_signature


def coherence_signature(x, y, fs=1.0, window='hann', *args, **kwds):
    return array_namespace(x, y, _skip_if_str_or_tuple(window))


def csd_signature(x, y, fs=1.0, window='hann', *args, **kwds):
    return array_namespace(x, y, _skip_if_str_or_tuple(window))


def periodogram_signature(x, fs=1.0, window='boxcar'):
    return array_namespace(x, _skip_if_str_or_tuple(window))


def welch_signature(x, fs=1.0, window='hann', *args, **kwds):
    return array_namespace(x, _skip_if_str_or_tuple(window))


def spectrogram_signature(x, fs=1.0, window=('tukey', 0.25), *args, **kwds):
    return array_namespace(x, _skip_if_str_or_tuple(window))


def stft_signature(x, fs=1.0, window='hann', *args, **kwds):
    return array_namespace(x, _skip_if_str_or_tuple(window))


def istft_signature(Zxx, fs=1.0, window='hann', *args, **kwds):
    return array_namespace(Zxx, _skip_if_str_or_tuple(window))


def resample_signature(x, num, t=None, axis=0, window=None, domain='time'):
    return array_namespace(x, t, _skip_if_str_or_tuple(window))


def resample_poly_signature(x, up, down, axis=0, window=('kaiser', 5.0), *args, **kwds):
    return array_namespace(x, _skip_if_str_or_tuple(window))


def check_COLA_signature(window, nperseg, noverlap, tol=1e-10):
    return array_namespace(_skip_if_str_or_tuple(window))


def check_NOLA_signature(window, nperseg, noverlap, tol=1e-10):
    return array_namespace(_skip_if_str_or_tuple(window))


def czt_signature(x, *args, **kwds):
    return array_namespace(x)

decimate_signature = czt_signature
gauss_spline_signature = czt_signature


def deconvolve_signature(signal, divisor):
    return array_namespace(signal, divisor)


def detrend_signature(data, axis=1, type='linear', bp=0, *args, **kwds):
    return array_namespace(data, _skip_if_int(bp))


def filtfilt_signature(b, a, x, *args, **kwds):
    return array_namespace(b, a, x)


def lfilter_signature(b, a, x, axis=-1, zi=None):
    return array_namespace(b, a, x, zi)


def find_peaks_signature(
    x, height=None, threshold=None, distance=None, prominence=None, width=None,
    wlen=None, rel_height=0.5, plateau_size=None
):
    return array_namespace(x, height, threshold, prominence, width, plateau_size)


def find_peaks_cwt_signature(
    vector, widths, wavelet=None, max_distances=None, *args, **kwds
):
    return array_namespace(vector, widths, max_distances)


def findfreqs_signature(num, den, N, kind='ba'):
    return array_namespace(num, den)


def firls_signature(numtaps, bands, desired, *, weight=None, fs=None):
    return array_namespace(bands, desired, weight)


def firwin_signature(numtaps, cutoff, *args, **kwds):
    return array_namespace(cutoff)


def firwin2_signature(numtaps, freq, gain, *args, **kwds):
    return array_namespace(freq, gain)


def freqs_zpk_signature(z, p, k, worN, *args, **kwds):
    return array_namespace(z, p, _skip_if_int(worN))

freqz_zpk_signature = freqs_zpk_signature


def freqs_signature(b, a, worN=200, *args, **kwds):
    return array_namespace(b, a, _skip_if_int(worN))

freqz_signature = freqs_signature


def freqz_sos_signature(sos, worN=512, *args, **kwds):
    return array_namespace(sos, _skip_if_int(worN))

sosfreqz_signature = freqz_sos_signature


def gausspulse_signature(t, *args, **kwds):
    arr_t = None if isinstance(t, str) else t
    return array_namespace(arr_t)


def group_delay_signature(system, w=512, whole=False, fs=6.283185307179586):
    return array_namespace(_skip_if_str_or_tuple(system), _skip_if_int(w))


def hilbert_signature(x, N=None, axis=-1):
    return array_namespace(x)

hilbert2_signature = hilbert_signature


def iirdesign_signature(wp, ws, *args, **kwds):
    return array_namespace(wp, ws)


def iirfilter_signature(N, Wn, *args, **kwds):
    return array_namespace(Wn)


def invres_signature(r, p, k, tol=0.001, rtype='avg'):
    return array_namespace(r, p, k)

invresz_signature = invres_signature


############################### XXX: excluded, blacklisted on CuPy (mismatched API)
def lfilter_zi_signature(b, a):
    return array_namespace(b, a)

def sosfilt_zi_signature(sos):
    return array_namespace(sos)

# needs to be blacklisted on CuPy (is not implemented)
def remez_signature(numtaps, bands, desired, *, weight=None, **kwds):
    return array_namespace(bands, desired, weight)
#############################################

def lfiltic_signature(b, a, y, x=None):
    return array_namespace(b, a, y, x)


def lombscargle_signature(
    x, y, freqs, precenter=False, normalize=False, *,
    weights=None, floating_mean=False
):
    return array_namespace(x, y, freqs, weights)


def lp2bp_signature(b, a, *args, **kwds):
    return array_namespace(b, a)

lp2bs_signature = lp2bp_signature
lp2hp_signature = lp2bp_signature
lp2lp_signature = lp2bp_signature

tf2zpk_signature = lp2bp_signature
tf2sos_signature = lp2bp_signature

normalize_signature = lp2bp_signature
residue_signature = lp2bp_signature 
residuez_signature = residue_signature


def lp2bp_zpk_signature(z, p, k, *args, **kwds):
    return array_namespace(z, p)

lp2bs_zpk_signature = lp2bp_zpk_signature
lp2hp_zpk_signature = lp2bs_zpk_signature
lp2lp_zpk_signature = lp2bs_zpk_signature


def zpk2sos_signature(z, p, k, *args, **kwds):
    return array_namespace(z, p)

zpk2ss_signature = zpk2sos_signature
zpk2tf_signature = zpk2sos_signature


def max_len_seq_signature(nbits, state=None, length=None, taps=None):
    return array_namespace(state, taps)


def medfilt_signature(volume, kernel_size=None):
    return array_namespace(volume)


def medfilt2d_signature(input, kernel_size=3):
    return array_namespace(input)


def minimum_phase_signature(h, *args, **kwds):
    return array_namespace(h)


def order_filter_signature(a, domain, rank):
    return array_namespace(a, domain)


def peak_prominences_signature(x, peaks, *args, **kwds):
    return array_namespace(x, peaks)


peak_widths_signature = peak_prominences_signature


def place_poles_signature(A, B, poles, method='YT', rtol=0.001, maxiter=30):
    return array_namespace(A, B, poles)


def savgol_filter_signature(x, *args, **kwds):
    return array_namespace(x)


def sawtooth_signature(t, width=1):
    return array_namespace(t)


def sepfir2d_signature(input, hrow, hcol):
    return array_namespace(input, hrow, hcol)


def sos2tf_signature(sos):
    return array_namespace(sos)


sos2zpk_signature = sos2tf_signature


def sosfilt_signature(sos, x, axis=-1, zi=None):
    return array_namespace(sos, x, zi)


def sosfiltfilt_signature(sos, x, *args, **kwds):
    return array_namespace(sos, x)


def spline_filter_signature(Iin, lmbda=5.0):
    return array_namespace(Iin)


def square_signature(t, duty=0.5):
    return array_namespace(t)


def ss2tf_signature(A, B, C, D, input=0):
    return array_namespace(A, B, C, D)

ss2zpk_signature = ss2tf_signature


def sweep_poly_signature(t, poly, phi=0):
    return array_namespace(t, _skip_if_poly1d(poly))


def symiirorder1_signature(signal, c0, z1, precision=-1.0):
    return array_namespace(signal)


def symiirorder2_signature(input, r, omega, precision=-1.0):
    return array_namespace(input)


def cspline1d_signature(signal, *args, **kwds):
    return array_namespace(signal)

qspline1d_signature = cspline1d_signature
cspline2d_signature = cspline1d_signature
qspline2d_signature = qspline1d_signature


def cspline1d_eval_signature(cj, newx, *args, **kwds):
    return array_namespace(cj, newx)

qspline1d_eval_signature = cspline1d_eval_signature


def tf2ss_signature(num, den):
    return array_namespace(num, den)


def unique_roots_signature(p, tol=0.001, rtype='min'):
    return array_namespace(p)


def upfirdn_signature(h, x, up=1, down=1, axis=-1, mode='constant', cval=0):
    return array_namespace(h, x)


def vectorstrength_signature(events, period):
    return array_namespace(events, period)


def wiener_signature(im, mysize=None, noise=None):
    return array_namespace(im)


def zoom_fft_signature(x, fn, m=None, *, fs=2, endpoint=False, axis=-1):
    return array_namespace(x, fn)
