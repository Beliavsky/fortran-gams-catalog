! GAMS I1a1a: RKF45 continuation and one-step modes against analytic IVPs.
program check_ode
 use ForsytheMalcolmMoler, only: RKF45
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 implicit none
 integer,parameter :: dp=selected_real_kind(10,50)
 integer :: problem,direction,mode,j,iflag,iw(5),calls,count,steps,evaluations
 real(dp),allocatable :: y(:),work(:),expected(:)
 real(dp) :: t,tout,relative,previous,error,maximum
 maximum=0;count=0;steps=0;evaluations=0
 do problem=1,2
  allocate(y(problem),work(3+6*problem),expected(problem))
  do direction=-1,1,2
   do mode=1,2
    y=0;y(1)=1;work=0;iw=0;t=0;relative=1.e-9_dp
    iflag=1;if(mode==2) iflag=-1
    if(mode==1) then
     do j=1,8
      tout=direction*0.25_dp*j
      call RKF45(rhs,y,t,tout,relative,1.e-11_dp,iflag,work,iw)
      if(iflag/=2 .or. t/=tout) error stop 'RKF45 interval status'
      call verify()
     end do
    else
     tout=direction*2._dp
     do calls=1,10000
      previous=t
      call RKF45(rhs,y,t,tout,relative,1.e-11_dp,iflag,work,iw)
      if(iflag/=-2 .and. iflag/=2) error stop 'RKF45 step status'
      if(direction*(t-previous)<=0) error stop 'RKF45 no directional progress'
      call verify()
      steps=steps+1
      if(iflag==2) exit
     end do
     if(iflag/=2 .or. t/=tout) error stop 'RKF45 step target'
    end if
   end do
  end do
  ! Initial zero-length request is allowed and must preserve the initial state.
  y=0;y(1)=1;work=0;iw=0;t=0;tout=0;relative=1.e-9_dp;iflag=1
  call RKF45(rhs,y,t,tout,relative,1.e-11_dp,iflag,work,iw)
  if(iflag/=2 .or. t/=0) error stop 'RKF45 initial equal-time request'
  call verify()
  deallocate(y,work,expected)
 end do
 ! Explicitly check the documented too-small-relative-tolerance recovery.
 problem=1;allocate(y(1),work(9),expected(1))
 y=1;work=0;iw=0;t=0;tout=1;relative=0;iflag=1
 call RKF45(rhs,y,t,tout,relative,1.e-11_dp,iflag,work,iw)
 if(iflag/=3 .or. relative<=0 .or. t/=0) error stop 'RKF45 tolerance adjustment'
 call RKF45(rhs,y,t,tout,relative,1.e-11_dp,iflag,work,iw)
 if(iflag/=2 .or. t/=tout) error stop 'RKF45 tolerance recovery'
 call verify()
 print '(a,i0)', 'Analytic ODE state comparisons: ',count
 print '(a,i0)', 'Accepted one-step returns: ',steps
 print '(a,i0)', 'Derivative evaluations: ',evaluations
 print '(a,es14.6)', 'Maximum normalized solution error: ',maximum
 print '(a)', 'PASS ode'
contains
 subroutine rhs(time,state,derivative)
  real(dp),intent(in) :: time,state(:)
  real(dp),intent(out) :: derivative(:)
  evaluations=evaluations+1
  if(problem==1) then
   derivative=-state
  else
   derivative(1)=state(2);derivative(2)=-state(1)
  end if
 end subroutine
 subroutine verify()
  if(.not.ieee_is_finite(t) .or. .not.all(ieee_is_finite(y))) error stop 'nonfinite ODE result'
  if(problem==1) then
   expected=exp(-t)
  else
   expected=[cos(t),-sin(t)]
  end if
  error=maxval(abs(y-expected))/max(1._dp,maxval(abs(expected)))
  maximum=max(maximum,error)
  if(error>5.e-8_dp) error stop 'ODE analytic mismatch'
  count=count+1
 end subroutine
end program
