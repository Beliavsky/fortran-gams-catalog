! GAMS J4: fftpack::hilbert for binary64 real input, analytic periodic signals.
program analytic
 use iso_fortran_env, only: real64
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 use fftpack, only: hilbert
 implicit none
 integer,parameter :: sizes(*)=[1,2,3,4,5,7,8,9,10,16,17]
 integer :: k,n,j,m,count
 real(real64),allocatable :: x(:)
 complex(real64),allocatable :: z(:),want(:)
 real(real64) :: angle,nyquist,error,maximum,pi
 maximum=0;count=0;pi=acos(-1._real64)
 do k=1,size(sizes)
  n=sizes(k)
  allocate(x(n),want(n))
  do m=0,(n-1)/2
   do j=0,n-1
    angle=2*pi*m*j/n
    nyquist=0
    if(mod(n,2)==0) nyquist=0.3_real64*(-1._real64)**j
    if(m==0) then
     x(j+1)=1.25_real64+nyquist
     want(j+1)=cmplx(x(j+1),0._real64,kind=real64)
    else
     x(j+1)=1.25_real64+0.7_real64*cos(angle)+0.2_real64*sin(angle)+nyquist
     want(j+1)=cmplx(x(j+1),0.7_real64*sin(angle)-0.2_real64*cos(angle),kind=real64)
    end if
   end do
   z=hilbert(x)
   if(size(z)/=n) error stop 'analytic signal size'
   if(.not.all(ieee_is_finite(real(z))) .or. .not.all(ieee_is_finite(aimag(z)))) error stop 'nonfinite analytic signal'
   error=maxval(abs(z-want))/max(1._real64,maxval(abs(want)))
   maximum=max(maximum,error)
   if(error>5.e-12_real64) error stop 'analytic signal mismatch'
   count=count+1
  end do
  deallocate(x,want,z)
 end do
 print '(a,i0)', 'Analytic periodic signal comparisons: ',count
 print '(a,es14.6)', 'Maximum normalized error: ',maximum
 print '(a)', 'PASS analytic'
end program
