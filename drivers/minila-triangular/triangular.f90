! GAMS D2a3: direct diagonal/triangular solvers in module prim.
program triangular
 use prim, only: diag_sub,fwd_sub,bck_sub
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 implicit none
 integer :: n,which,scale_case,i,j,count
 real,allocatable :: a(:,:),original(:,:),b(:),expected(:),got(:)
 real :: scale,solution_error,residual,maximum_error,maximum_residual,denom
 real,parameter :: tolerance=5.e-6
 count=0;maximum_error=0;maximum_residual=0
 do n=1,12
  allocate(a(n,n),original(n,n),b(n),expected(n))
  do i=1,n
   expected(i)=(-1.0)**i*(0.5+real(i)/7)
  end do
  do which=1,3
   do scale_case=1,3
    select case(scale_case)
    case(1);scale=1
    case(2);scale=1.e-8
    case(3);scale=1.e8
    end select
    a=0
    do i=1,n
     a(i,i)=scale*(4+real(i)/3)
     do j=1,n
      if(which==2 .and. j<i) a(i,j)=scale*0.02*real(mod(i+2*j,5)-2)
      if(which==3 .and. j>i) a(i,j)=scale*0.02*real(mod(2*i+j,5)-2)
     end do
    end do
    original=a;b=matmul(a,expected)
    select case(which)
    case(1);got=diag_sub(a,b)
    case(2);got=fwd_sub(a,b)
    case(3);got=bck_sub(a,b)
    end select
    if(size(got)/=n .or. .not.all(ieee_is_finite(got))) error stop 'invalid triangular result'
    if(any(a/=original)) error stop 'input matrix was modified'
    solution_error=maxval(abs(got-expected))/maxval(abs(expected))
    denom=maxval(sum(abs(a),dim=2))*maxval(abs(got))+maxval(abs(b))
    residual=maxval(abs(matmul(a,got)-b))/denom
    maximum_error=max(maximum_error,solution_error);maximum_residual=max(maximum_residual,residual)
    if(solution_error>tolerance .or. residual>tolerance) error stop 'triangular reference mismatch'
    count=count+1
   end do
  end do
  deallocate(a,original,b,expected,got)
 end do
 print '(a,i0)', 'Default REAL storage bits: ',storage_size(1.0)
 print '(a,i0)', 'Checked triangular systems: ',count
 print '(a,es14.6)', 'Maximum relative solution error: ',maximum_error
 print '(a,es14.6)', 'Maximum scaled residual: ',maximum_residual
 print '(a)', 'PASS triangular'
end program
