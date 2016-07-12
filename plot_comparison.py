import numpy as np
import pylab as pl
import sys

from model import generic_prediction, ReadTransitionData
from observation import obs_spec 
from process_fits import read_mcmc_fits, write_mcmc_stats

def plot_spec():

    c = 299792.485

    mcmc_chain_fname = obs_spec.chain_fname
    best_logN = read_mcmc_fits(mcmc_chain_fname,'logN')
    best_b = read_mcmc_fits(mcmc_chain_fname,'b')
    best_z = read_mcmc_fits(mcmc_chain_fname,'z')
    
    alpha = np.array([best_logN,best_b,best_z])
    print('logN = %.2f' % best_logN)
    print('b    = %.2f' % best_b)
    print('z    = %.5f' % best_z)
    print('\n')

    model_flux = generic_prediction(alpha,obs_spec)

    # Use the first transition as the central wavelength
    rest_wave = obs_spec.transitions_params_array[0][0][1]
    obs_spec_dv = c*(obs_spec.wave - rest_wave) / rest_wave

    summary = raw_input('Write best fit summary? (y/n): ')
    if summary == 'y':
        output_summary_fname = obs_spec.spec_path + '/vpfit_mcmc/bestfits_summary.dat' 
        write_mcmc_stats(mcmc_chain_fname,output_summary_fname)

    plotting = raw_input('Plot model comparison? (y/n): ')
    if plotting == 'y':
        pl.step(obs_spec_dv,obs_spec.flux,'k',label=r'$\rm Data$')
        pl.step(obs_spec_dv,model_flux,'b',lw=1.5,label=r'$\rm Best\,Fit$')
        pl.step(obs_spec_dv,obs_spec.dflux,'r')
        pl.axhline(1,ls='--',c='g',lw=1.2)
        pl.axhline(0,ls='--',c='g',lw=1.2)
        pl.ylim([-0.1,1.4])
        dv = float(raw_input('Enter velocity range: '))
        pl.xlim([-dv,dv])
        pl.xlabel(r'$dv\,[km/s]$')
        pl.ylabel(r'$\rm Flux$')
        pl.legend(loc='best')
        pl.savefig(obs_spec.spec_path + '/vpfit_mcmc/bestfit_spec.pdf',bbox_inches='tight',dpi=100)
        print('Written %svpfit_mcmc/bestfit_spec.pdf\n' % obs_spec.spec_path)
    
    output_model = raw_input('Write best fit model spectrum? (y/n): ')
    if output_model == 'y':
        np.savetxt(obs_spec.spec_path + '/vpfit_mcmc/bestfit_model.dat',
                np.c_[obs_spec.wave,obs_spec.flux, obs_spec.dflux, model_flux],
                header='wave\tflux\terror\tmodel')
        print('Written %svpfit_mcmc/bestfit_model.dat\n' % obs_spec.spec_path)
def main():
    plot_spec()

if __name__ == '__main__':
    sys.exit(int(main() or 0))