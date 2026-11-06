program minimization
  use ForsytheMalcolmMoler, only: BrentMin, Fmin
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer, parameter :: dp=selected_real_kind(10,50)
  real(dp), parameter :: centers(3)=[-3.0_dp,0.0_dp,4.0_dp]
  real(dp), parameter :: widths(3)=[0.25_dp,1.0_dp,3.0_dp]
  real(dp), parameter :: scales(3)=[1e-6_dp,1.0_dp,1e6_dp]
  real(dp) :: center,width,amplitude,x,fx,a,b,location_error,value_error
  real(dp) :: max_location,max_value,fresh
  integer :: ic,iw,is,shape,api,calls,neval,status,count,total_calls,probe_calls
  max_location=0; max_value=0; count=0; total_calls=0
  do ic=1,3
    center=centers(ic)
    do iw=1,3
      width=widths(iw); a=center-width; b=center+1.5_dp*width
      do is=1,3
        amplitude=scales(is)
        do shape=1,4
          do api=1,2
            calls=0
            if(api==1)then
              call BrentMin(a,b,objective,1e-10_dp*width,500,neval,status,x,fx)
              if(status/=0)error stop 'Unexpected minimizer status'
              if(neval/=calls)error stop 'Objective evaluation count differs'
            else
              x=Fmin(a,b,objective,1e-10_dp*width)
              fx=objective(x)
            end if
            total_calls=total_calls+calls
            if(.not.ieee_is_finite(x).or..not.ieee_is_finite(fx))error stop 'Nonfinite result'
            if(x<a.or.x>b)error stop 'Result outside search interval'
            location_error=abs(x-center)/width
            fresh=objective(x)
            value_error=abs(fresh)/amplitude
            if(location_error>5e-5_dp)error stop 'Known minimizer location check failed'
            if(value_error>1e-8_dp)error stop 'Known minimum value check failed'
            if(abs(fx-fresh)>1e-12_dp*amplitude)error stop 'Reported objective disagrees'
            max_location=max(max_location,location_error)
            max_value=max(max_value,value_error)
            count=count+1
          end do
        end do
      end do
    end do
  end do
  ! Deliberately expose the pinned routine's misleading exhaustion status.
  center=0.2_dp; width=1; amplitude=1; shape=1; calls=0
  call BrentMin(-1.0_dp,1.0_dp,objective,1e-12_dp,1,neval,status,x,fx)
  probe_calls=calls
  if(status/=0.or.abs(x-center)<1e-3_dp)error stop 'Pinned exhaustion behavior changed'
  if(neval/=probe_calls)error stop 'Probe evaluation count differs'
  print '(a,i0)', 'Known-minimum API comparisons: ',count
  print '(a,es14.6)', 'Maximum width-normalized location error: ',max_location
  print '(a,es14.6)', 'Maximum amplitude-normalized objective error: ',max_value
  print '(a,i0)', 'Normal-case objective calls (excluding independent fresh checks): ',total_calls
  print '(a,i0,a,es14.6)', 'One-iteration probe status: ',status,'; location error: ',abs(x-center)
  print '(a)', 'WARNING: BrentMin does not report iteration exhaustion; Fmin discards status.'
  print '(a)', 'PASS minimization'
contains
  function objective(arg) result(value)
    real(dp), intent(in) :: arg
    real(dp) :: value,t
    calls=calls+1
    t=(arg-center)/width
    select case(shape)
    case(1)
      value=t*t
    case(2)
      value=t**4
    case(3)
      value=exp(t)-t-1.0_dp
    case(4)
      value=t*t*(1.0_dp+0.1_dp*t+0.05_dp*t*t)
    end select
    value=amplitude*value
  end function
end program
