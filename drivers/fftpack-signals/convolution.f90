! GAMS J2: fftpack::conv checked against direct finite convolution.
program convolution
 use iso_fortran_env, only: real64
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 use fftpack, only: conv
 implicit none
 integer :: nx,ny,i,j,count
 real(real64), allocatable :: x(:),y(:),r(:),reference(:)
 complex(real64), allocatable :: z(:),w(:),c(:),creference(:)
 real(real64) :: error,maximum
 maximum=0;count=0
 do nx=1,7
  do ny=1,7
   allocate(x(nx),y(ny),reference(nx+ny-1),z(nx),w(ny),creference(nx+ny-1))
   do i=1,nx
    x(i)=(-1._real64)**i*real(i,real64)/3
    z(i)=cmplx(x(i),0.1_real64*i,kind=real64)
   end do
   do j=1,ny
    y(j)=0.2_real64*j-0.7_real64
    w(j)=cmplx(y(j),-0.15_real64*j,kind=real64)
   end do
   reference=0;creference=0
   do i=1,nx
    do j=1,ny
     reference(i+j-1)=reference(i+j-1)+x(i)*y(j)
     creference(i+j-1)=creference(i+j-1)+z(i)*w(j)
    end do
   end do
   r=conv(x,y);c=conv(z,w)
   if(size(r)/=nx+ny-1 .or. size(c)/=nx+ny-1) error stop 'convolution size'
   if(.not.all(ieee_is_finite(r))) error stop 'nonfinite real convolution'
   if(.not.all(ieee_is_finite(real(c))) .or. .not.all(ieee_is_finite(aimag(c)))) error stop 'nonfinite complex convolution'
   error=maxval(abs(r-reference))/max(1._real64,maxval(abs(reference)))
   maximum=max(maximum,error)
   if(error>5.e-12_real64) error stop 'real convolution mismatch'
   error=maxval(abs(c-creference))/max(1._real64,maxval(abs(creference)))
   maximum=max(maximum,error)
   if(error>5.e-12_real64) error stop 'complex convolution mismatch'
   count=count+2
   deallocate(x,y,reference,z,w,creference,r,c)
  end do
 end do
 print '(a,i0)', 'Direct convolution comparisons: ',count
 print '(a,es14.6)', 'Maximum normalized error: ',maximum
 print '(a)', 'PASS convolution'
end program
