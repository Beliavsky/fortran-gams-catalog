! GAMS H2a1a1: adaptive QUANC8 checked against analytic definite integrals.
program quadrature
 use ForsytheMalcolmMoler, only: Quanc8
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 implicit none
 integer,parameter :: dp=selected_real_kind(10,50)
 integer :: power,which,interval,nofun,count,total_evaluations
 real(dp) :: a,b,expected,value,errest,flag,error,maximum
 maximum=0;count=0;total_evaluations=0;which=0
 do power=0,12
  do interval=1,4
   select case(interval)
   case(1);a=0;b=1
   case(2);a=-1;b=2
   case(3);a=2;b=-1
   case(4);a=1;b=1
   end select
   expected=(b**(power+1)-a**(power+1))/real(power+1,dp)
   call check()
  end do
 end do
 do which=1,3
  select case(which)
  case(1);a=-1;b=1;expected=exp(1._dp)-exp(-1._dp)
  case(2);a=0;b=acos(-1._dp);expected=2
  case(3);a=0;b=1;expected=acos(-1._dp)/4
  end select
  call check()
 end do
 print '(a,i0)', 'Analytic integral comparisons: ',count
 print '(a,i0)', 'Function evaluations: ',total_evaluations
 print '(a,es14.6)', 'Maximum normalized error: ',maximum
 print '(a)', 'PASS quadrature'
contains
 function integrand(x) result(y)
  real(dp),intent(in) :: x
  real(dp) :: y
  select case(which)
  case(0);y=x**power
  case(1);y=exp(x)
  case(2);y=sin(x)
  case(3);y=1/(1+x*x)
  end select
 end function
 subroutine check()
  call Quanc8(integrand,a,b,1.e-11_dp,1.e-11_dp,value,errest,nofun,flag)
  if(.not.ieee_is_finite(value) .or. .not.ieee_is_finite(errest) .or. .not.ieee_is_finite(flag)) error stop 'nonfinite quadrature'
  if(flag/=0 .or. errest<0 .or. nofun<0) error stop 'quadrature status'
  if(a==b .and. nofun/=0) error stop 'zero interval evaluation count'
  if(a/=b .and. nofun<=0) error stop 'missing function evaluations'
  error=abs(value-expected)/max(1._dp,abs(expected))
  maximum=max(maximum,error)
  if(error>5.e-10_dp) error stop 'analytic integral mismatch'
  total_evaluations=total_evaluations+nofun
  count=count+1
 end subroutine
end program
